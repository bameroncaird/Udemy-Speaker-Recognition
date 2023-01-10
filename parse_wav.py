"""
This file contains my implementation for Assignment 3, "Parse a WAV file."
I am just using the struct module and basic Python.
Actually, I did not even use struct.
See for checking if correct: https://gist.github.com/eerwitt/ba51e181d50de6555a2ae613a558c0b6
"""
import struct

def parse_wav(filename):

    with open(filename, "rb") as f:
        raw_bytes = f.read()

    
    # see the following for info to get the required info from the file
    # I am just reporting what was asked in the course
    # http://soundfile.sapp.org/doc/WaveFormat/
    chunk_size = int.from_bytes(raw_bytes[4:8], byteorder="little")
    num_channels = int.from_bytes(raw_bytes[22:24], byteorder="little")
    sample_rate = int.from_bytes(raw_bytes[24:28], byteorder="little")
    audio = raw_bytes[44:]
    bits_per_sample = int.from_bytes(raw_bytes[34:36], byteorder="little")
    total_num_bytes = int.from_bytes(raw_bytes[40:44], byteorder="little")

    # the first sample is the first two bytes
    # see other values for why (every sample is 2 bytes, or 16 bits, long)
    first_sample = int.from_bytes(audio[:2], byteorder="little")

    # calculate length in seconds
    num_samples = total_num_bytes / 2
    length_seconds = num_samples / sample_rate

    print(f"Chunk Size = {chunk_size}")
    print(f"Number of Channels = {num_channels}")
    print(f"Sample Rate = {sample_rate}")
    print(f"Bits per Sample = {bits_per_sample}")
    print(f"Total Number of Bytes = {total_num_bytes}")
    print(f"First Sample = {first_sample}")
    print(f"Number of Samples = {num_samples}")
    print(f"Length in Seconds = {length_seconds}")


parse_wav("male_audio.wav")


#############################################
# Checker function from GitHub


def parse_wave_raw(filename):
    # Open the example wave file stored in the current directory.
    with open(filename, 'rb') as wav_file:
        # Main Header
        chunk_id = wav_file.read(4)
        assert chunk_id == b'RIFF', 'RIFF little endian, RIFX big endian: assume RIFF'

        chunk_size = struct.unpack('<I', wav_file.read(4))[0]

        wav_format = wav_file.read(4)
        assert wav_format == b'WAVE', wav_format

        # Sub Chunk 1
        sub_chunk_1_id = wav_file.read(4)
        assert sub_chunk_1_id == b'fmt ', sub_chunk_1_id

        sub_chunk_1_size = struct.unpack('<I', wav_file.read(4))[0]

        audio_format = struct.unpack('<H', wav_file.read(2))[0]
        assert audio_format == 1, '1 == PCM Format: assumed PCM'

        num_channels = struct.unpack('<H', wav_file.read(2))[0]
        assert num_channels == 1, '1 == Mono, 2 == Stereo: assumed Mono'

        sample_rate = struct.unpack('<I', wav_file.read(4))[0]
        # assert sample_rate == 16000, 'assumed 16000'

        byte_rate = struct.unpack('<I', wav_file.read(4))[0]
        # assert byte_rate == 32000, byte_rate

        # Could this be something other than an int?
        block_align = struct.unpack('<H', wav_file.read(2))[0]
        assert block_align == 2, block_align

        bits_per_sample = struct.unpack('<H', wav_file.read(2))[0]
        assert bits_per_sample == 16, bits_per_sample

        # Sub Chunk 2
        sub_chunk_2_id = wav_file.read(4)
        assert sub_chunk_2_id == b'data', sub_chunk_2_id

        sub_chunk_2_size = struct.unpack('<I', wav_file.read(4))[0]

        samples = []
        bytes_per_sample = bits_per_sample / 8
        assert (sub_chunk_2_size % bytes_per_sample) == 0, 'Uneven sample size'

        sample_count = int(sub_chunk_2_size / bytes_per_sample)

        for _ in range(sample_count):
            samples.append(struct.unpack('<h', wav_file.read(2))[0])

        assert chunk_size == (
                len(wav_format) +
                len(sub_chunk_1_id) + sub_chunk_1_size + 4 +  # Full size of subchunk 1
                len(sub_chunk_2_id) + sub_chunk_2_size + 4 # Full size of subchunk 2
            ), chunk_size

        assert sub_chunk_1_size == (
                2 +  # audio_format
                2 +  # num_channels
                4 +  # sample_rate
                4 +  # byte_rate
                2 +  # block_align
                2  # bits_per_sample
            ), sub_chunk_1_size

        bytes_per_sample = bits_per_sample / 8
        assert byte_rate == (
                sample_rate * num_channels * bytes_per_sample
            ), byte_rate

        assert block_align == (
                num_channels * bytes_per_sample
            ), block_align
        

        
        assert sub_chunk_2_size == (
            len(samples) * bytes_per_sample 
        ), sub_chunk_2_size

        length_in_seconds = (
            len(samples) / sample_rate
        )

        print('''
Parsed {filename}
-----------------------------------------------
Channels: {num_channels}
Sample Rate: {sample_rate}
First Sample: {first_sample}
Second Sample: {second_sample}
Length in Seconds: {length_in_seconds}'''.format(
            filename=filename,
            num_channels=num_channels,
            sample_rate=sample_rate,
            first_sample=samples[0],
            second_sample=samples[1],
            length_in_seconds=length_in_seconds))


print("\n\n\n\n\n\n")
parse_wave_raw("male_audio.wav")