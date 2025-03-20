from astropy.io import fits
import numpy as np
import argparse
from datetime import datetime

# Define polynomial coefficients for each band (Updated with new coefficients)
POLY_COEFFS = {
    'Band-2': (-2.83, 33.564, -18.026, 3.588),  # Updated coefficients for Band 2
    'Band-3': (-2.939, 33.312, -16.659, 3.066),  # Updated coefficients for Band 3
    'Band-4': (-3.190, 38.642, -20.471, 3.964),  # Updated coefficients for Band 4
    'Band-5': (-2.608, 27.357, -13.091, 2.368),  # Updated coefficients for Band 5
}

# def find_freq(header):
#     """
#     Find frequency value in the FITS header.
#     """
#     print("Searching for frequency in the header...")
    
#     # Try to find frequency in common places
#     for i in range(5):
#         ctype_key = 'CTYPE%i' % i
#         crval_key = 'CRVAL%i' % i
#         if ctype_key in header and 'FREQ' in header[ctype_key]:
#             freq = header.get(crval_key)
#             return freq
    
#     # If not found, look for specific keywords
#     freq = header.get('RESTFRQ') or header.get('FREQ')
#     if freq:
#         return freq
    
#     # If nothing found, print and return None
#     print("Frequency not found in the header.")
#     return None


# def flatten(filename, channel=0, freqaxis=0):
#     """Flatten a FITS file to create a 2D image. Returns new header and data."""
#     from astropy.wcs import WCS

#     with fits.open(filename) as f:
#         naxis = f[0].header['NAXIS']
#         if naxis < 2:
#             raise ValueError('Cannot make map from this FITS file.')
#         if naxis == 2:
#             return f[0].header, f[0].data

#         w = WCS(f[0].header)
#         wn = WCS(naxis=2)

#         wn.wcs.crpix[0] = w.wcs.crpix[0]
#         wn.wcs.crpix[1] = w.wcs.crpix[1]
#         wn.wcs.cdelt = w.wcs.cdelt[0:2]
#         wn.wcs.crval = w.wcs.crval[0:2]
#         wn.wcs.ctype[0] = w.wcs.ctype[0]
#         wn.wcs.ctype[1] = w.wcs.ctype[1]

#         header = wn.to_header()
#         header["NAXIS"] = 2
#         header["NAXIS1"] = f[0].header['NAXIS1']
#         header["NAXIS2"] = f[0].header['NAXIS2']
#         copy = ('EQUINOX', 'EPOCH')
#         for k in copy:
#             r = f[0].header.get(k)
#             if r:
#                 header[k] = r

#         dataslice = []
#         for i in range(naxis, 0, -1):
#             if i <= 2:
#                 dataslice.append(np.s_[:],)
#             elif i == freqaxis:
#                 dataslice.append(channel)
#             else:
#                 dataslice.append(0)

#         header["FREQ"] = find_freq(f[0].header)

#         try:
#             header["BMAJ"] = f[0].header['BMAJ']
#             header["BMIN"] = f[0].header['BMIN']
#             header["BPA"] = f[0].header['BPA']
#         except KeyError:
#             pass

#         return header, f[0].data[tuple(dataslice)]

def get_band_coefficients(frequency_ghz):
    """Determine the band's polynomial coefficients based on frequency in GHz."""
    if 0.125 <= frequency_ghz < 0.25:
        return POLY_COEFFS['Band-2']
    elif 0.25 <= frequency_ghz < 0.5:
        return POLY_COEFFS['Band-3']
    elif 0.55 <= frequency_ghz < 0.85:
        return POLY_COEFFS['Band-4']
    elif 1.05 <= frequency_ghz < 1.45:
        return POLY_COEFFS['Band-5']
    else:
        raise ValueError(f'Frequency {frequency_ghz} GHz not in known bands.')

def primary_beam_model(frequency_ghz, radius_arcmin, coeffs):
    """Calculate the primary beam model based on polynomial coefficients."""
    a, b, c, d = coeffs
    # Compute correction using the polynomial formula
    correction = 1 + (a / 1e3) * (radius_arcmin * frequency_ghz)**2 + \
                     (b / 1e7) * (radius_arcmin * frequency_ghz)**4 + \
                     (c / 1e10) * (radius_arcmin * frequency_ghz)**6 + \
                     (d / 1e13) * (radius_arcmin * frequency_ghz)**8
    return correction


# ANSI escape codes for colors
RESET = "\033[0m"
GREEN = "\033[92m"
YELLOW = "\033[93m"
RED = "\033[91m"
CYAN = "\033[96m"
MAGENTA = "\033[95m"



def get_frequencies(header):
    """
    Extract all frequency information from the FITS header.
    Returns list of frequencies in Hz.
    """
    print(f"{YELLOW}Gathering relevant information from the FITS image......................{RESET}")
    
    frequencies = []
    
    # First check for direct FREQ keys (FREQ0001, etc.)
    freq_keys = [key for key in header.keys() if key.startswith('FREQ') and len(key) > 4]
    if freq_keys:
        frequencies = [float(header[key]) for key in sorted(freq_keys)]
        return frequencies
    
    # If no direct FREQ keys, check for frequency axis
    for i in range(header['NAXIS']):
        ctype_key = f'CTYPE{i+1}'
        if ctype_key in header and 'FREQ' in header[ctype_key]:
            freq_axis = i + 1
            crval = float(header[f'CRVAL{freq_axis}'])  # Reference frequency
            cdelt = float(header[f'CDELT{freq_axis}'])  # Frequency increment
            naxis = int(header[f'NAXIS{freq_axis}'])    # Number of channels
            
            # Generate frequency array
            frequencies = [crval + (i * cdelt) for i in range(naxis)]
            return frequencies
    
    # If still no frequencies found, try single frequency value
    freq = header.get('RESTFRQ') or header.get('FREQ')
    if freq:
        return [float(freq)]
        
    return None


def flatten_cube(filename):
    """Flatten a FITS file but preserve frequency planes. Returns clean header and cube data."""
    from astropy.wcs import WCS

    with fits.open(filename) as f:
        naxis = f[0].header['NAXIS']
        if naxis < 2:
            raise ValueError('Cannot make map from this FITS file.')

        w = WCS(f[0].header)
        wn = WCS(naxis=3)  # Keep 3 dimensions for cube

        # Copy spatial dimensions WCS info
        wn.wcs.crpix[0] = w.wcs.crpix[0]
        wn.wcs.crpix[1] = w.wcs.crpix[1]
        wn.wcs.cdelt[:2] = w.wcs.cdelt[0:2]
        wn.wcs.crval[:2] = w.wcs.crval[0:2]
        wn.wcs.ctype[0] = w.wcs.ctype[0]
        wn.wcs.ctype[1] = w.wcs.ctype[1]

        if naxis > 2:  # Handle frequency axis for cubes
            wn.wcs.crpix[2] = w.wcs.crpix[2]
            wn.wcs.cdelt[2] = w.wcs.cdelt[2]
            wn.wcs.crval[2] = w.wcs.crval[2]
            wn.wcs.ctype[2] = w.wcs.ctype[2]

        header = wn.to_header()
        header["NAXIS"] = 3 if naxis > 2 else 2
        header["NAXIS1"] = f[0].header['NAXIS1']
        header["NAXIS2"] = f[0].header['NAXIS2']
        if naxis > 2:
            header["NAXIS3"] = f[0].header['NAXIS3']

        # Copy essential header info
        copy = ('EQUINOX', 'EPOCH', 'BMAJ', 'BMIN', 'BPA', 'FREQ')
        for k in copy:
            r = f[0].header.get(k)
            if r:
                header[k] = r

        # Fix ALTRVAL keyword if it exists
        if 'ALTRVAL' in f[0].header:
            try:
                val = float(f[0].header['ALTRVAL'])
                if val == float('-inf'):
                    header['ALTRVAL'] = -1e30  # Use a very large negative number instead
                else:
                    header['ALTRVAL'] = val
            except:
                header['ALTRVAL'] = -1e30

        # For cube, keep all frequency planes
        if naxis > 2:
            return header, f[0].data
        else:
            # For 2D, keep original flatten behavior
            return header, f[0].data[tuple([0] * (naxis-2) + [slice(None)]*2)]

def correct_fits_with_primary_beam(input_fits, output_fits, beam_threshold=0.01):
    """Apply primary beam correction to a FITS file."""
    print(f"{MAGENTA}Developed by Arpan Pal at NCRA-TIFR in 2024.{RESET}")
    print(f"{CYAN}Starting the attack !!!!{RESET}")
    print(f"{YELLOW}Gathering relevant information from the FITS image......................{RESET}")

    # Get data and clean header using flatten_cube
    header, data = flatten_cube(input_fits)
    
    # Get frequency information from the header
    frequency_hz = find_freq(header)
    if frequency_hz is None:
        raise ValueError('Frequency information (FREQ) not found in the FITS header.')
    frequency_ghz = frequency_hz / 1e9  # Convert to GHz
    print(f"{GREEN}Found frequency: {frequency_ghz:.2f} GHz{RESET}")

    # Calculate the pixel scale (separation per pixel in arcmin)
    pixel_scale_deg = abs(header['CDELT1'])  # Degrees per pixel
    pixel_scale_arcmin = pixel_scale_deg * 60  # Arcminutes per pixel
    print(f"{GREEN}Pixel scale: {pixel_scale_arcmin:.4f} arcmin/pixel{RESET}")
    
    # Generate a grid of pixel positions
    y, x = np.indices(data.shape[-2:])
    x_center = header['CRPIX1'] - 1
    y_center = header['CRPIX2'] - 1
    r = np.sqrt((x - x_center)**2 + (y - y_center)**2) * pixel_scale_arcmin

    # Create output array with same shape as input
    corrected_data = np.zeros_like(data)

    # Process each plane (or single image)
    if data.ndim == 2:
        coeffs = get_band_coefficients(frequency_ghz)
        print(f"{GREEN}Using polynomial coefficients: {coeffs}{RESET}")
        beam = primary_beam_model(frequency_ghz, r, coeffs)
        print(f"{GREEN}Calculated Beams!{RESET}")

        with np.errstate(divide='ignore', invalid='ignore'):
            corrected_data = np.where(np.abs(beam) >= beam_threshold, data / beam, 0)
        print(f"{GREEN}Beams applied to input FITS image !!!{RESET}")

    else:
        num_planes = data.shape[0]
        print(f"{GREEN}Processing {num_planes} frequency planes{RESET}")

        for i in range(num_planes):
            print(f"{CYAN}Processing plane {i+1}/{num_planes} at {frequency_ghz:.3f} GHz{RESET}")
            coeffs = get_band_coefficients(frequency_ghz)
            print(f"{GREEN}Using polynomial coefficients: {coeffs}{RESET}")
            
            beam = primary_beam_model(frequency_ghz, r, coeffs)
            
            with np.errstate(divide='ignore', invalid='ignore'):
                corrected_data[i] = np.where(np.abs(beam) >= beam_threshold,
                                           data[i] / beam, 0)
            print(f"{GREEN}Beam applied to plane {i+1}!{RESET}")

    # Update header history
    header['HISTORY'] = f"finalflash v0.3.2 {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"

    # Write corrected data
    fits.writeto(output_fits, corrected_data, header, overwrite=True, output_verify='ignore')
    print(f"{GREEN}Primary beam corrected FITS {'cube' if data.ndim > 2 else 'image'} saved to {output_fits}{RESET}")
    print(f"{MAGENTA}Finalflash done 💥💥💥💥💥💥{RESET}")


# def correct_fits_with_primary_beam(input_fits, output_fits, beam_threshold=0.01):
#     """Apply primary beam correction to a FITS file."""
#     print(f"{MAGENTA}Developed by Arpan Pal at NCRA-TIFR in 2024.{RESET}")
#     print(f"{CYAN}Starting the attack !!!!{RESET}")
#     print(f"{YELLOW}Gathering relevant information from the FITS image......................{RESET}")

#     # Flatten the FITS file to a 2D image, but keep the original header
#     original_header = fits.getheader(input_fits)
#     header, data = flatten(input_fits)
    
#     # Add the FinalFlash version and date to the end of the FITS history
#     version_info = f"finalflash v0.3.1 {datetime.now().strftime('%Y-%m-%dT%H:%M:%S')}"
#     original_header.append(('HISTORY', version_info), end=True)  # Append at the end of the header
    
#     # Get frequency information from the header (assuming CRVAL3 holds frequency in Hz)
#     frequency_hz = find_freq(header)
#     if frequency_hz is None:
#         raise ValueError('Frequency information (FREQ) not found in the FITS header.')
#     frequency_ghz = frequency_hz / 1e9  # Convert to GHz
#     print(f"{GREEN}Found frequency: {frequency_ghz:.2f} GHz{RESET}")

#     # Determine which band's coefficients to use based on the frequency
#     band_coeffs = get_band_coefficients(frequency_ghz)
#     print(f"{GREEN}Using polynomial coefficients for {frequency_ghz} GHz: {band_coeffs}{RESET}")

#     # Calculate the pixel scale (separation per pixel in arcmin)
#     pixel_scale_deg = abs(header['CDELT1'])  # Degrees per pixel
#     pixel_scale_arcmin = pixel_scale_deg * 60  # Arcminutes per pixel
#     print(f"{GREEN}Pixel scale: {pixel_scale_arcmin:.4f} arcmin/pixel{RESET}")
    
#     # Generate a grid of pixel positions
#     y, x = np.indices(data.shape)
#     x_center = header['CRPIX1'] - 1
#     y_center = header['CRPIX2'] - 1
#     r = np.sqrt((x - x_center)**2 + (y - y_center)**2) * pixel_scale_arcmin  # Radius in arcmin
    
#     # Compute the primary beam model for each pixel
#     beam = primary_beam_model(frequency_ghz, r, band_coeffs)
#     print(f"{GREEN}Calculated Beams!{RESET}")

#     # Check where the absolute value of the beam is less than the threshold
#     with np.errstate(divide='ignore', invalid='ignore'):
#         corrected_data = np.where(np.abs(beam) >= beam_threshold, data / beam, 0)
#     print(f"{GREEN}Beams applied to input FITS image !!!{RESET}")

#     # Check the original data type and adjust the BITPIX accordingly
#     original_dtype = data.dtype
#     if original_dtype == np.dtype('>f4'):
#         original_header['BITPIX'] = -32  # 32-bit float
#         corrected_data = corrected_data.astype('>f4')
#     elif original_dtype == np.dtype('>f2'):
#         original_header['BITPIX'] = 16  # 16-bit integer
#         corrected_data = corrected_data.astype('>i2')
#     elif original_dtype == np.dtype('>f8'):
#         original_header['BITPIX'] = -64  # 64-bit float
#         corrected_data = corrected_data.astype('>f8')
#     else:
#         raise ValueError(f"{RED}Unsupported data type: {original_dtype}{RESET}")

#     # Write the corrected data to a new FITS file with the original header
#     fits.writeto(output_fits, corrected_data, original_header, overwrite=True)
#     print(f"{GREEN}Primary beam corrected FITS file saved to {output_fits}{RESET}")
#     print(f"{MAGENTA}Finalflash done 💥💥💥💥💥💥{RESET}")


def main():
    parser = argparse.ArgumentParser(description='Apply primary beam correction to a FITS image.')
    parser.add_argument('input_image', type=str, help='Path to the input FITS image file')
    parser.add_argument('output_image', type=str, help='Path to the output FITS image file')
    args = parser.parse_args()

    correct_fits_with_primary_beam(args.input_image, args.output_image)

if __name__ == "__main__":
    main()
