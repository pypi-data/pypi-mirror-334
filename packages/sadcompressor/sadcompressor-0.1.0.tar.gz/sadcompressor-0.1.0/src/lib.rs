use pyo3::prelude::*;
use pyo3::exceptions::PyOverflowError;

/////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
/// Reimplementation of encoder module functions.

/// Encode unsigned integer 'number'. Tries to use least possible number of bytes, removing leading zeros in the number.
/// Given number = (a0 a1 a2 a3 a4 a5 a6 a7) written as sequency of bytes, 
/// write it in the form (c a(n+1) a(n+2) .. a7) where all elements ak = 0 for k<n.
/// The highest term is obtained by merging length of the number and an:
/// c = (l0 l1 l(lengthbits-1) an(lengthbits) an(lengthbits+1) .. an(7)), written in bit form.
/// Here l = max(0, n-minbytes).     
/// 
/// Args:
///     number (u64): integer to encode.
///     minbytes (u8): least number of bytes used by encoded number.
///     lengthbits (u8): number of bits to store length of the integer.
/// 
/// Raises:
///     OverflowError: if number is very large.
/// 
/// Returns:
///     bytes: encoded integer
#[pyfunction]
fn encode_uint(number: u64, minbytes: u8, lengthbits: u8) -> PyResult<Vec<u8>> {
    if lengthbits>3 { // More than bits in byte.
        return Err(PyOverflowError::new_err("'lengthbits' should not be larger than 8."));
    }
    if minbytes>8 { // Larger than u64 length.
        return Err(PyOverflowError::new_err("'minbytes' should not be larger than 8."));
    }
    // Convert `number` to bytes array.
    let buf: [u8; 8] = number.to_be_bytes(); // 8 = number of bytes in u64 
    let mut first: u8 = 0; // First nonzero byte.
    for n in 0..usize::from(8-minbytes) {
        if buf[n] != 0 { break; }
        first += 1;
    }
    // Compute length sufficient to store the number.
    let mut length: u8 = 8 - first;
    let mut prefix: u8;
    let lennum: u8 = 8-lengthbits;
    if length>0 {
        prefix = buf[usize::from(first)];
        if lengthbits>0 {
            let mask : u8 = (1<<lennum) - 1; // Bits that can be used by number.
            let masked: u8 = prefix&mask;
            if masked!=prefix { // Save length into additional byte.
                prefix = 0;
                length += 1;
            } else {
                prefix = masked;
                first += 1;
            };
        } else {
            first += 1;
        }
    } else {
        prefix = 0;
        length += 1;
    }
    // Compute number of additional bytes.
    let l:u8 = if length>minbytes {length-minbytes} else {0}; 
    let maxlength: u8 = 1<<lengthbits;
    if l>=maxlength {
        return Err(PyOverflowError::new_err("lengthbits is not enough to store number of bits."));
    }
    // Save length.
    if lengthbits>0 {
        prefix |= l<<lennum;
    }
    // Create output buffer.
    let mut b = vec![prefix];
    b.extend_from_slice(&buf[usize::from(first)..8]);
    return Ok(b);
}

/// Decode unsigned integer encoded with `encode_uint`.
/// Args:
///     data (bytes): output of encode_uint concatenated with arbitrary data. Encoded integer must be prefix of the data.
///     minbytes (int), lengthbits (int): see `encode_uint`
/// Raises:
///     OverflowError: if `data` is shorter than expected integer length.
/// Result:
///     number (int): decoded integer
///     length (int): number of bytes consumed by the decoder from `data`
#[pyfunction]
fn decode_uint<'a>(data: &'a[u8], minbytes: u8, lengthbits: u8) -> PyResult<(u64, &'a[u8])> {
    if lengthbits>8 {
        return Err(PyOverflowError::new_err("Number length can not be more than 8 bits."))
    }
    let length:usize = ( ( if lengthbits>0 { data[0] >> (8-lengthbits) } else { 0 } ) + minbytes ).into();
    if data.len()<length {
        return Err(PyOverflowError::new_err("Incomplete number."))
    } 
    let mut number:u64 = (data[0] & ( if lengthbits>0 { (1<<(8-lengthbits)) - 1 } else {0xff} )).into();
    for i in 1..length {
        let a: u64 = data[i].into();
        number = (number << 8) | a;
    }
    Ok( (number, &data[length..]) )
}

/// Encoder.py remake
#[pyfunction]
fn maxbytes_uint(minbytes: u8, lengthbits: u8) -> PyResult<u8> {
    Ok( minbytes + ( 1 << lengthbits ) - 1 )
}

/////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
/// Reimplementation of frames module functions.

#[pyfunction]
fn round_nbits(nbits:u8) -> PyResult<u8> {
    let res: u8 = match nbits {
        0..=1 => 1,
        2 => 2,
        3..=4 => 4,
        5..=8 => 8,
        n @ 7.. => n,
    };
    return Ok(res);
}

// fn pack_bits<'a>(data:&'a[u8], nbits: u8) -> PyResult<()> {
//     if nbits>=8: return data, 0
//     assert 8%nbits==0
//     packet_size = 8//nbits
//     data = data.flatten()
//     sz = int(np.ceil(data.size/packet_size))
//     mask = (1<<nbits) - 1
//     result = np.zeros(sz, dtype=np.uint8)
//     for n in range(packet_size):
//         d = data[n::packet_size]
//         result[:len(d)] |= (d&mask)<<(n*nbits)
//     ncut = sz*packet_size - data.size
//     return result, ncut
// }

// def unpack_bits(data, nbits, ncut):
//     # return data
//     if nbits>=8: return data    
//     packet_size = 8//nbits
//     mask = (1<<nbits) - 1
//     data = data.flatten()
//     result = np.zeros(data.size*packet_size, dtype=np.uint8)
//     for n in range(packet_size):
//         result[n::packet_size] = (data>>(n*nbits))&mask 
//     return result if ncut<=0 else result[:-ncut]

// def find_bitfixes(data):
//     msk = np.bitwise_or.reduce(data.flatten())
//     bitspervalue = data.dtype.itemsize*8
//     nsufix = 0
//     for n in range(bitspervalue):
//         if (1<<n)&msk: break
//         else: nsufix+=1
//     nprefix = 0
//     for n in range(bitspervalue):
//         if (1<<(bitspervalue-n-1))&msk: break
//         else: nprefix+=1
//     return nprefix, nsufix, bitspervalue


/////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
/// Module declaration.

/// A Python module implemented in Rust.
#[pymodule]
#[pyo3(name="_rusted")]
fn sadcompressor(m: &Bound<'_, PyModule>) -> PyResult<()> {
    m.add_function(wrap_pyfunction!(decode_uint, m)?)?;
    m.add_function(wrap_pyfunction!(encode_uint, m)?)?;
    m.add_function(wrap_pyfunction!(maxbytes_uint, m)?)?;

    m.add_function(wrap_pyfunction!(round_nbits, m)?)?;

    Ok(())
}
