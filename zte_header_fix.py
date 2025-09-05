import sys

def compare_bin_files(file1_path, file2_path, bytes_to_compare=192):
    """
    Compare the first 192 bytes of two binary files, automatically overwrite file2
    to match file1 at differing positions, and display differences with filenames.
    
    Args:
        file1_path (str): Path to the first binary file (Original File).
        file2_path (str): Path to the second binary file (Edited File).
        bytes_to_compare (int): Number of bytes to compare (default: 192).
    """
    try:
        # Read the first 192 bytes from both files
        with open(file1_path, 'rb') as f1:
            data1 = f1.read(bytes_to_compare)
        
        with open(file2_path, 'rb') as f2:
            data2 = f2.read(bytes_to_compare)
        
        # Check if files have enough bytes
        if len(data1) < bytes_to_compare or len(data2) < bytes_to_compare:
            print(f"Error: One or both files have fewer than {bytes_to_compare} bytes.")
            print(f"Original File ({file1_path}) size: {len(data1)} bytes")
            print(f"Edited File ({file2_path}) size: {len(data2)} bytes")
            return
        
        # Compare bytes and collect differences
        differences = []
        for i in range(bytes_to_compare):
            if data1[i] != data2[i]:
                differences.append((i, data1[i], data2[i]))
        
        # Output results and handle overwrite
        if not differences:
            print("ZTE Headers are Equal")
        else:
            print(f"Comparing files:")
            print(f"Original File: {file1_path}")
            print(f"Edited File: {file2_path}")
            print(f"Found {len(differences)} differences in the first 192 bytes:")
            print("Position | Original File Byte | Edited File Byte")
            print("-" * 45)
            for pos, byte1, byte2 in differences:
                print(f"0x{pos:04x}   | 0x{byte1:02x}             | 0x{byte2:02x}")
            
            # Automatically overwrite file2
            try:
                with open(file2_path, 'r+b') as f2:
                    for pos, byte1, _ in differences:
                        f2.seek(pos)
                        f2.write(bytes([byte1]))
                # Print "ZTE Header Fixed" in lime green (ANSI escape code)
                print("\033[92mZTE Header Fixed\033[0m")
            except PermissionError:
                print(f"Error: Permission denied when writing to {file2_path}.")
            except Exception as e:
                print(f"Error: Failed to update {file2_path} - {e}")
                
    except FileNotFoundError as e:
        print(f"Error: File not found - {e}")
    except Exception as e:
        print(f"Error: An unexpected error occurred - {e}")

if __name__ == "__main__":
    # Check if correct number of arguments is provided
    if len(sys.argv) != 3:
        print("Usage: python compare_bin_files.py <file1.bin> <file2.bin>")
        sys.exit(1)
    
    # Get file paths from command-line arguments
    file1_path = sys.argv[1]
    file2_path = sys.argv[2]
    
    # Run comparison
    compare_bin_files(file1_path, file2_path)