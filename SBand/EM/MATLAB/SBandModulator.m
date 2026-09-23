% HSTX Modulation Pipeline
% 
% Data -> V.35 Scrambler -> Diff. Encoder -> 1/2 Rate Convolutional Encoder
%               OQPSK Modulation <- Pulse Shaping Filter <-
%

%% Modulation Parameters
sps = 2; % 4 Samples per symbol
dataRate = 10000000000; % 10Mbps max data rate
rollOff = 0.35;
numFilt = 32;


%% Block Definitions

% V.35 Scrambler
scrambler = comm.Scrambler(2, ...
    '1 + Z^-18 + Z^-23', ...
    [0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 1]);

% Differential Encoder
diffEnc = comm.DifferentialEncoder;

% 1/2 Rate Convolutional Encoder
trellis = poly2trellis(7, [171 133]);
convEnc = comm.ConvolutionalEncoder(trellis);

% OQPSK Modulator (and Pulse Shaping)
oqpskMod = comm.OQPSKModulator(...
    "BitInput", true, ...
    "SamplesPerSymbol", sps, ...
    "PulseShape", "Root raised cosine",...
    "RolloffFactor", rollOff, ...
    "FilterSpanInSymbols", numFilt);

%% Pipeline

%dataBits = transpose(reshape(dec2bin(0:255,8).' - '0', 1, []));

dataBits = ones(1, 1000);
dataBits(1:100) = 0;
dataBits = transpose(repmat(dataBits, 1, 10000));


% 0 0 0 1 1 0 1 1 repeated ~4 seconds each
% dataBits = transpose(horzcat(repmat([0 0], 1, 10000000), ...
%            repmat([0 1], 1, 10000000), ...
%            repmat([1 0], 1, 10000000), ...
%            repmat([1 1], 1, 10000000)));

% dataBits = ones(10000000, 1);
% dataBits(1:1000000) = 0;


% dataBits = randi(2,[1000 1]) - 1;

% dataBits = transpose(repmat([0 0 0 1 1 0 1 1], 1, 1000));

% txSignal = oqpskMod(convEnc(diffEnc(scrambler(dataBits))));
txSignal = transpose(oqpskMod(dataBits));

%% Save Signal
% Ensure txSignal is single precision (32-bit float per component)
txSignalSingle = single(txSignal);

% Interleave I and Q components into a 1D vector: [I1, Q1, I2, Q2, ...]
iqInterleaved = zeros(2 * length(txSignalSingle), 1, 'single');
iqInterleaved(1:2:end) = real(txSignalSingle);
iqInterleaved(2:2:end) = imag(txSignalSingle);

% % Calculate filter delay in samples
% filterDelay = (oqpskMod.FilterSpanInSymbols * oqpskMod.SamplesPerSymbol) / 2;
% 
% % Trim leading delay samples from the signal
% txSignalTrimmed = txSignal(filterDelay + 1 : end);

% txSignalTrimmed = txSignal(25:end);

% Save to binary file
filename = 'oqpsk_tx_signal_01long_2sps.fc32';
fileID = fopen(filename, 'wb');
fwrite(fileID, iqInterleaved, 'float32');
fclose(fileID);


fid = fopen(filename, 'rb');

% Skip the first 512 bytes
fseek(fid, 1024/32 * numFilt, 'bof');

% Read the remainder
data = fread(fid, Inf, '*uint8');
fclose(fid);

% Overwrite the original file
fid = fopen(filename, 'wb');  % 'wb' truncates the file
fwrite(fid, data, 'uint8');
fclose(fid);

fprintf('Saved %d complex samples to %s\n', length(txSignal), filename);

constViewer = comm.ConstellationViewer(...
    'SamplesPerSymbol', sps, ...          % Sets downsampling/trajectory visualization (e.g., 8)
    'SymbolsToDisplay', 1000, ...          % Number of symbols shown on screen at once
    'ShowReferenceConstellation', true, ...% Show ideal QPSK constellation points for reference
    'ReferenceConstellation', [1+1i 1-1i -1+1i -1-1i]/sqrt(2), ... % Standard QPSK reference
    'Title', 'OQPSK Signal Constellation (Pre-Demodulation)');

%% 2. Display the Signal
% Pass the IQ complex signal into the viewer
constViewer(iqInterleaved);

