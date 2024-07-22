# EST_UHF
Demodulation scripts of the UHF Ground Station of the EPFL Spacecraft Team

This GNU Radio script uses the gr-satellites and gr-gpredict-doppler libraries.

## Soapy PLUTO Source
This block interfaces the script with the PlutoSDR, providing input parameters
such as the sample rate and the center frequency for the local oscillator. The
output is an IQ signal from the measurements of the SDR. For this FSK demodulation, the sample rate is set to 96 kHz, which is ten times the expected
symbol rate. Although most FSK beacons have a baud rate of 9600, the sample
rate should be adapted for each application. According to the Shannon-Nyquist
theorem, this sample rate should be at least twice the desired signal frequency.
However, it is generally set at five to ten times the symbol rate. The bandwidth
parameter is set to the sample rate to ensure efficient use of computational resources. The desired center frequency for signal acquisition is transmitted to
this block through a variable updated by the Gpredict Doppler block. If another
SDR is used in the future, the SoapySDR library contains other SDR interfacing
blocks.

## Frequency Shift
After testing this script on multiple satellite passes, a frequency offset appeared
in certain measurements, which can be explained by inaccuracies in the TLE
information provided by the network. Manual correction can be applied to center
the signal. The default frequency shift is zero.

## FSK Demodulator
This demodulation block, fetched from the gr-satellites library, replaces the
Frequency Xlating FIR Filter and the Quadrature Demod blocks from Section
3.1.2. FSK signals are detected and converted into floating point values. The
input is the baud rate, set at 9600. This demodulator can work with both float
and complex inputs.

## Binary Slicer
The floating point values are converted into binary data (0 or 1).

## NRZI Decode
This block performs NRZI decoding as described in Section 3.4.

## Descrambler
This block descrambles the bits to retrieve the original signal. The descrambler
uses the G3RUH descrambling algorithm, which is represented as the mask 0x21
and a length of 16.

## HDLC Deframer
This deframer takes the input bit stream and converts it into packets. These
packets are sent out as Protocol Data Units (PDU), which are now decoded data
streams.

## Message Debug
This block prints messages to the GNU Radio terminal for easy debugging. This
block is temporary, as currently we do not process the packets and only display
them in a terminal, as seen in Figure 4.2.

## Gpredict Doppler
Real-time Doppler correction is essential in LEO satellite communication as the
frequency offset reaches 10 kHz for most passes. Compared to the frequency deviations and bandwidths used in FSK modulation, this offset is non-negligible. This
block is fetched from the gr-gpredict-doppler library [6] and offers the possibility
to modify a variable through a Message Pair to Variable block. The frequency
input is sent from the Gpredict Radio Control running on the remote client PC.

## TCP Sink
This block establishes the TCP transmission with the other instance of GNU Radio running on the remote client PC. Here the block is disabled for demonstration
purposes.

## File Sink
This block records the IQ samples of the signal throughout the acquisition. Logging and storing this information is crucial in a mission, as it offers the opportunity to reprocess the signal later in case of poor demodulation. However,
depending on the sample rate, these files can become very large. A storage server accessible through the EPFL network should be set up to facilitate the logging
(at least temporarily) of these passes.
