#!/usr/bin/python2
#

from gnuradio import gr, uhd
from gnuradio import eng_notation
from gnuradio.eng_option import eng_option
from optparse import OptionParser
from gnuradio import blocks

import sys
import nutaq

class psdr_interface():
	def __init__(self, target_id, reference=0, card=1, rx_freq=943e6, rx_datarate=8e6, rx_calibrate=1, rx_band=0, rx_lna_gain=2 , rx_vga1_gain=1, rx_gain2=16, rx_gain3=4, rx_rf_filter=2, rx_lpf_bandwith=6,
				 tx_freq=943e6, tx_datarate=8e6, tx_calibrate=1, tx_band=0, tx_vga1_gain=-10, tx_vga2_gain=15, tx_gain3=3, tx_lpf_bandwith=6):

		self.set_target_id(target_id) 
		self.set_reference(reference)
		self.set_card(card) 
		self.set_rx_freq(rx_freq) 
		self.set_rx_datarate(rx_datarate) 
		self.set_rx_calibrate(rx_calibrate) 
		self.set_rx_band(rx_band) 
		self.set_rx_lna_gain(rx_lna_gain) 
		self.set_rx_vga1_gain(rx_vga1_gain) 
		self.set_rx_gain2(rx_gain2) 
		self.set_rx_gain3(rx_gain3)
		self.set_rx_rf_filter(rx_rf_filter) 
		self.set_rx_lpf_bandwith(rx_lpf_bandwith) 
		self.set_tx_freq(tx_freq)
		self.set_tx_datarate(tx_datarate) 
		self.set_tx_calibrate(tx_calibrate) 
		self.set_tx_band(tx_band) 
		self.set_tx_vga1_gain(tx_vga1_gain) 
		self.set_tx_vga2_gain(tx_vga2_gain) 
		self.set_tx_gain3(tx_gain3) 
		self.set_tx_lpf_bandwith(tx_lpf_bandwith)

		self.custom_registers = dict()

		self.nutaq_radio420_tx = nutaq.radio420_tx(self._target_id, card, 0)
		self.nutaq_radio420_tx.set_default_enable(1)
		self.nutaq_radio420_tx.set_default_tx_freq(self._tx_freq)
		self.nutaq_radio420_tx.set_default_reference(self._reference)
		self.nutaq_radio420_tx.set_default_datarate(self._tx_datarate)
		self.nutaq_radio420_tx.set_default_calibrate(self._tx_calibrate)
		self.nutaq_radio420_tx.set_default_band(self._tx_band)
		self.nutaq_radio420_tx.set_default_update_rate(1)
		self.nutaq_radio420_tx.set_default_tx_vga1_gain(self._tx_vga1_gain)
		self.nutaq_radio420_tx.set_default_tx_vga2_gain(self._tx_vga2_gain)
		self.nutaq_radio420_tx.set_default_tx_gain3(self._tx_gain3)
		self.nutaq_radio420_tx.set_default_tx_lpf_bandwidth(self._tx_lpf_bandwith)
		self.nutaq_radio420_tx.set_default_ref_clk_ctrl(0)
		self.nutaq_radio420_tx.set_default_rf_ctrl(0)
		self.nutaq_radio420_tx.set_default_tx_gain_ctrl(0)
		self.nutaq_radio420_tx.set_default_pll_cpld_ctrl(0)

		self.nutaq_radio420_rx = nutaq.radio420_rx(self._target_id, card, 1)
		self.nutaq_radio420_rx.set_default_enable(1)
		self.nutaq_radio420_rx.set_default_rx_freq(self._rx_freq)
		self.nutaq_radio420_rx.set_default_reference(self._reference)
		self.nutaq_radio420_rx.set_default_datarate(self._rx_datarate)
		self.nutaq_radio420_rx.set_default_calibrate(self._rx_calibrate)
		self.nutaq_radio420_rx.set_default_band(self._rx_band)
		self.nutaq_radio420_rx.set_default_update_rate(1)
		self.nutaq_radio420_rx.set_default_rx_lna_gain(self._rx_lna_gain)
		self.nutaq_radio420_rx.set_default_rx_vga1_gain(self._rx_vga1_gain)
		self.nutaq_radio420_rx.set_default_rx_gain2(self._rx_gain2)
		self.nutaq_radio420_rx.set_default_rx_gain3(self._rx_gain3)
		self.nutaq_radio420_rx.set_default_rx_rf_filter(self._rx_rf_filter)
		self.nutaq_radio420_rx.set_default_rx_lpf_bandwidth(self._rx_lpf_bandwith)
		self.nutaq_radio420_rx.set_default_ref_clk_ctrl(0)
		self.nutaq_radio420_rx.set_default_rf_ctrl(0)
		self.nutaq_radio420_rx.set_default_rx_gain_ctrl(0)
		self.nutaq_radio420_rx.set_default_pll_cpld_ctrl(0)


	def set_custom_register(self, index, value=0):
		"""Set a custom register for _target_id"""
		if (index in self.custom_registers):
			sys.stderr.write("WARNING : Custom register " + str(index) + " is already declared for " + self._target_id +"\n")
			return False

		custom_register = nutaq.custom_register(self._target_id, 2)
		custom_register.set_index(index)
		custom_register.set_default_value(value)
		custom_register.set_update_rate(1)

		self.custom_registers[index] = custom_register

		return True;

	def get_custom_register(self, index):
		"""Return the custom register index of _target_id"""
		if (index not in self.custom_registers):
			sys.stderr.write("WARNING : Custom register " + str(index) + " is not declared for " + self._target_id +"\n")
			return None

		return self.custom_registers[index]


	def set_target_id(self, target_id):
		"""This set target_id as the block ID of carrier board : string"""
		self._target_id = target_id

	def get_target_id(self):
		"""Return the block ID of carrier board : string"""
		return self._target_id
	
	
	def set_reference(self, reference):
		"""This set the reference source for the Radio420 PLL. The reference clock can be the internal 30.72 MHz oscillator or be the input reference at Rin external connector.
		0 -> internal
		1 -> external"""
		if ((reference == 0) or (reference == 1)):
			self._reference = reference
		else:
			sys.stderr.write("\nERROR : %s reference must be 0 (internal) or 1 (external) so it can't be %s !\n" % (self._target_id, reference))
			sys.exit(1)

	def get_reference(self):
		"""This return the reference source for the Radio420 PLL. The reference clock can be the internal 30.72 MHz oscillator or be the input reference at Rin external connector.
		0 -> internal
		1 -> external"""		
		return self._reference
	

	def set_card (self, card):
		"""This set the card number of the Radio420 (1 or 2)"""
		if ((card == 1) or (card == 2)):
			self._card = card
		else:
			sys.stderr.write("\nERROR : %s card number must be 1 or 2 so it can't be %s !\n" % (self._target_id, card))
			sys.exit(1)

	def get_card (self, card):
		"""This return the card number of the Radio420 (1 or 2)"""
		return self._card
	
	
	def set_rx_freq(self, rx_freq):
		"""This set the center frequency of the signal that is received by the Radio420 (carrier frequency)."""
		try:
			float(rx_freq)
			self._rx_freq = rx_freq
		except ValueError:
			sys.stderr.write("\nERROR : %s rx_freq must be a float so it can't be %s !\n" % (self._target_id, rx_freq))
			sys.exit(1)

	def get_rx_freq(self, rx_freq):
		"""This return the center frequency of the signal that is received by the Radio420 (carrier frequency)."""
		return self._rx_freq
	
	
	def set_rx_datarate(self, rx_datarate):
		"""This set the data rate from the DAC and to the ADC. Since the signal is interleaved (IQ), the acquisition frequency is half of the data rate."""
		try:
			float(rx_datarate)
			self._rx_datarate = rx_datarate
		except ValueError:
			sys.stderr.write("\nERROR : %s rx_datarate must be a float so it can't be %s !\n" % (self._target_id, rx_datarate))
			sys.exit(1)

	def get_rx_datarate(self, rx_datarate):
		"""This return the data rate from the DAC and to the ADC. Since the signal is interleaved (IQ), the acquisition frequency is half of the data rate."""
		return self._rx_datarate
	

	def set_rx_calibrate (self, rx_calibrate):
		"""This set automatic calibration. When automatic calibration is enabled, a calibration algorithm will be run during initialization to minimize LO leakage, IQ gain and phase imbalance.
		0 -> disabled
		1 -> enabled"""
		if ((rx_calibrate == 0) or (rx_calibrate == 1)):
			self._rx_calibrate = rx_calibrate
		else:
			sys.stderr.write("\nERROR : %s rx_calibrate must be 0 (disabled) or 1 (enabled) so it can't be %s !\n" % (self._target_id, rx_calibrate))
			sys.exit(1)

	def get_rx_calibrate (self, rx_calibrate):
		"""This return automatic calibration. When automatic calibration is enabled, a calibration algorithm will be run during initialization to minimize LO leakage, IQ gain and phase imbalance.
		0 -> disabled
		1 -> enabled"""
		return self._rx_calibrate
	

	def set_rx_band(self, rx_band):
		"""This set the optimal RF path for your signal. Low band is better matched for signal from 300 to 1500 MHz and high band is better for signal from 1500 to 3000 MHz.
		0 -> low band
		1 -> high band"""
		if ((rx_band == 0) or (rx_band == 1)):
			self._rx_band = rx_band
		else:
			sys.stderr.write("\nERROR : %s rx_band must be 0 (Low band) or 1 (High band) so it can't be %s !\n" % (self._target_id, rx_band))
			sys.exit(1)

	def get_rx_band(self, rx_band):
		"""This return the optimal RF path for your signal. Low band is better matched for signal from 300 to 1500 MHz and high band is better for signal from 1500 to 3000 MHz.
		0 -> low band
		1 -> high band"""
		return self._rx_band
	

	def set_rx_lna_gain(self, rx_lna_gain):
		"""This set the Receive Low Noise Amplifier gain
		1 -> ByPass
		2 -> Medium gain
		3 -> Maximum Gain"""
		if ((rx_lna_gain == 1) or (rx_lna_gain == 2) or (rx_lna_gain == 3)):
			self._rx_lna_gain = rx_lna_gain
		else:
			sys.stderr.write("\nERROR : %s rx_lna_gain must be 1 (ByPass), 2 (Medium Gain) or 3 (Maximum Gain) so it can't be %s !\n" % (self._target_id, rx_lna_gain))
			sys.exit(1)

	def get_rx_lna_gain(self, rx_lna_gain):
		"""This return the Receive Low Noise Amplifier gain
		1 -> ByPass
		2 -> Medium gain
		3 -> Maximum Gain"""
		return self._rx_lna_gain


	def set_rx_vga1_gain (self, rx_vga1_gain):
		"""This set the Receive amplifier 1. Can be set to 5 dB, 19 dB or 30 dB.
		1 -> 5 dB
		2 -> 19 dB
		3 -> 30 dB"""
		if ((rx_vga1_gain == 1) or (rx_vga1_gain == 2) or (rx_vga1_gain == 3)):
			self._rx_vga1_gain = rx_vga1_gain
		else:
			sys.stderr.write("\nERROR : %s rx_vga1_gain must be 1 (5 dB), 2 (19 dB) or 3 (30 dB) so it can't be %s !\n" % (self._target_id, rx_vga1_gain))
			sys.exit(1)

	def get_rx_vga1_gain (self, rx_vga1_gain):
		"""This return the Receive amplifier 1. Can be set to 5 dB, 19 dB or 30 dB.
		1 -> 5 dB
		2 -> 19 dB
		3 -> 30 dB"""
		return self._rx_vga1_gain
	

	def set_rx_gain2(self, rx_gain2):
		"""This set Receive amplifier 2. Can be set from 0 to 30 dB."""
		if (rx_gain2 in range(31)):
			self._rx_gain2 = rx_gain2
		else:
			sys.stderr.write("\nERROR : %s rx_gain2 must be an integer between 0 and 30 so it can't be %s !\n" % (self._target_id, rx_gain2))
			sys.exit(1)			

	def get_rx_gain2(self, rx_gain2):
		"""This return Receive amplifier 2. Can be set from 0 to 30 dB."""
		return self._rx_gain2
	

	def set_rx_gain3(self, rx_gain3):
		"""This set Receive amplifier 3. Can be set from -13 dB to 18 dB."""
		if (rx_gain3 in range(-13, 19)):
			self._rx_gain3 = rx_gain3
		else:
			sys.stderr.write("\nERROR : %s rx_gain3 must be an integer between -13 and 18 so it can't be %s !\n" % (self._target_id, rx_gain3))
			sys.exit(1)		
		
	def get_rx_gain3(self, rx_gain3):
		"""This return Receive amplifier 3. Can be set from -13 dB to 18 dB."""
		return self._rx_gain3
	
	def set_rx_rf_filter(self, rx_rf_filter):
		"""This set a band-pass filter from the filter bank.
		0 -> (Fc = 882 MHz BW = 25 MHz)(Fc = 2140 MHz BW = 60 MHz)
		1 -> (Fc = 837 MHz BW = 25 MHz)(Fc = 1950 MHz BW = 60 MHz)
		2 -> No filter - bypass filter bank
		3 -> (Fc = 943 MHz BW = 35 MHz)(Fc = 1960 MHz BW = 60 MHz)
		4 -> (Fc = 898 MHz BW = 35 MHz)(Fc = 1880 MHz BW = 60 MHz)
		5 -> (Fc = 915 MHz BW = 26 MHz)(Fc = 2495 MHz BW = 390 MHz)
		6 -> (Fc = 782 MHz BW = 10 MHz)(Fc = 1748 MHz BW = 75 MHz)
		7 -> (Fc = 751 MHz BW = 10 MHz)(Fc = 1843 MHz BW = 75 MHz)"""
		if (rx_rf_filter in range(8)):
			self._rx_rf_filter = rx_rf_filter
		else:
			sys.stderr.write("\nERROR : %s rx_rf_filter must be an integer between 0 and 7 so it can't be %s !\n" % (self._target_id, rx_rf_filter))
			sys.exit(1)		
		
	def get_rx_rf_filter(self, rx_rf_filter):
		"""This return the band-pass filter from the filter bank.
		0 -> (Fc = 882 MHz BW = 25 MHz)(Fc = 2140 MHz BW = 60 MHz)
		1 -> (Fc = 837 MHz BW = 25 MHz)(Fc = 1950 MHz BW = 60 MHz)
		2 -> No filter - bypass filter bank
		3 -> (Fc = 943 MHz BW = 35 MHz)(Fc = 1960 MHz BW = 60 MHz)
		4 -> (Fc = 898 MHz BW = 35 MHz)(Fc = 1880 MHz BW = 60 MHz)
		5 -> (Fc = 915 MHz BW = 26 MHz)(Fc = 2495 MHz BW = 390 MHz)
		6 -> (Fc = 782 MHz BW = 10 MHz)(Fc = 1748 MHz BW = 75 MHz)
		7 -> (Fc = 751 MHz BW = 10 MHz)(Fc = 1843 MHz BW = 75 MHz)"""
		return self.rx_rf_filter
	

	def set_rx_lpf_bandwith(self, rx_lpf_bandwith):
		"""This set a configurable analog filter within the RX path. You may set it to any value in the available list. The values are bandwidths on each side of the center frequencies.
		0 -> 28 MHz
		1 -> 20 MHz
		2 -> 14 MHz
		3 -> 12 MHz
		4 -> 10 MHz
		5 -> 8.75 MHz
		6 -> 7 MHz
		7 -> 6 MHz
		8 -> 5.5 MHz
		9 -> 5 MHz
		10 -> 3.84 MHz
		11 -> 3 MHz
		12 -> 2.75 MHz
		13 -> 2.5 MHz
		14 -> 1.75 MHz
		15 -> 1.5 MHz
		16 -> Bypass"""
		if (rx_lpf_bandwith in range(17)):
			self._rx_lpf_bandwith = rx_lpf_bandwith
		else:
			sys.stderr.write("\nERROR : %s rx_lpf_bandwith must be an integer between 0 and 16 so it can't be %s !\n" % (self._target_id, rx_lpf_bandwith))
			sys.exit(1)		

	def get_rx_lpf_bandwith(self, rx_lpf_bandwith):
		"""This return the configurable analog filter within the RX path. You may set it to any value in the available list. The values are bandwidths on each side of the center frequencies.
		0 -> 28 MHz
		1 -> 20 MHz
		2 -> 14 MHz
		3 -> 12 MHz
		4 -> 10 MHz
		5 -> 8.75 MHz
		6 -> 7 MHz
		7 -> 6 MHz
		8 -> 5.5 MHz
		9 -> 5 MHz
		10 -> 3.84 MHz
		11 -> 3 MHz
		12 -> 2.75 MHz
		13 -> 2.5 MHz
		14 -> 1.75 MHz
		15 -> 1.5 MHz
		16 -> Bypass"""
		return self._rx_lpf_bandwith
	
	def set_tx_freq(self, tx_freq):
		"""This set the center frequency of the signal that is emitted by the Radio420 (carrier frequency)."""
		try:
			float(tx_freq)
			self._tx_freq = tx_freq
		except ValueError:
			sys.stderr.write("\nERROR : %s tx_freq must be a float so it can't be %s !\n" % (self._target_id, tx_freq))
			sys.exit(1)

	def get_tx_freq(self, tx_freq):
		"""This return the center frequency of the signal that is emitted by the Radio420 (carrier frequency)."""
		return self._tx_freq
	

	def set_tx_datarate(self, tx_datarate):
		"""This set the data rate from the DAc and to the ADC. Since the signal is interleaved (IQ), the acquisition frequency is half of the data rate."""
		try:
			float(tx_datarate)
			self._tx_datarate = tx_datarate
		except ValueError:
			sys.stderr.write("\nERROR : %s tx_datarate must be a float so it can't be %s !\n" % (self._target_id, tx_datarate))
			sys.exit(1)

	def get_tx_datarate(self, tx_datarate):
		"""This return the data rate from the DAC and to the ADC. Since the signal is interleaved (IQ), the acquisition frequency is half of the data rate."""
		return self._tx_datarate
	

	def set_tx_calibrate (self, tx_calibrate):
		"""This set automatic calibration. When automatic calibration is enabled, a calibration algorithm will be run during initialization to minimize LO leakage, IQ gain and phase imbalance.
		0 -> disabled
		1 -> enabled"""
		if ((tx_calibrate == 0) or (tx_calibrate == 1)):
			self._tx_calibrate = tx_calibrate
		else:
			sys.stderr.write("\nERROR : %s tx_calibrate must be 0 (disabled) or 1 (enabled) so it can't be %s !\n" % (self._target_id, tx_calibrate))
			sys.exit(1)

	def get_tx_calibrate (self, tx_calibrate):
		"""This return automatic calibration. When automatic calibration is enabled, a calibration algorithm will be run during initialization to minimize LO leakage, IQ gain and phase imbalance.
		0 -> disabled
		1 -> enabled"""
		return self._tx_calibrate


	def set_tx_band(self, tx_band):
		"""This set the optimal RF path for your signal. Low band is better matched for signal from 300 to 1500 MHz and high band is better for signal from 1500 to 3000 MHz
		0 -> low band
		1 -> high band"""
		if ((tx_band == 0) or (tx_band == 1)):
			self._tx_band = tx_band
		else:
			sys.stderr.write("\nERROR : %s tx_band must be 0 (Low band) or 1 (High band) so it can't be %s !\n" % (self._target_id, tx_band))
			sys.exit(1)
	def get_tx_band(self, tx_band):
		"""This return the optimal RF path for your signal. Low band is better matched for signal from 300 to 1500 MHz and high band is better for signal from 1500 to 3000 MHz
		0 -> low band
		1 -> high band"""
		return self._tx_band
	
	def set_tx_vga1_gain(self, tx_vga1_gain):
		"""This set the Transmit amplifier 1. Can be set from -35 dB to -4 dB."""
		if (tx_vga1_gain in range(-35, -4)):
			self._tx_vga1_gain = tx_vga1_gain
		else:
			sys.stderr.write("\nERROR : %s tx_vga1_gain must be an integer between -35 and -4 so it can't be %s !\n" % (self._target_id, tx_vga1_gain))
			sys.exit(1)		

	def get_tx_vga1_gain(self, tx_vga1_gain):
		"""This return the Transmit amplifier 1. Can be set from -35 dB to -4 dB."""
		return self._tx_vga1_gain
	
	def set_tx_vga2_gain(self, tx_vga2_gain):
		"""This set the Transmit amplifier 2. Can be set from 0 dB to 25 dB."""
		if (tx_vga2_gain in range(0, 26)):
			self._tx_vga2_gain = tx_vga2_gain
		else:
			sys.stderr.write("\nERROR : %s tx_vga2_gain must be an integer between 0 and 25 so it can't be %s !\n" % (self._target_id, tx_vga2_gain))
			sys.exit(1)	

	def get_tx_vga2_gain(self, tx_vga2_gain):
		"""This return the Transmit amplifier 2. Can be set from 0 dB to 25 dB."""
		return self._tx_vga2_gain
	
	def set_tx_gain3(self, tx_gain3):
		"""This set the Transmit amplifier 3. Can be set from -13 dB to 18 dB."""
		if (tx_gain3 in range(-13, 19)):
			self._tx_gain3 = tx_gain3
		else:
			sys.stderr.write("\nERROR : %s tx_gain3 must be an integer between -13 and 18 so it can't be %s !\n" % (self._target_id, tx_gain3))
			sys.exit(1)	

	def get_tx_gain3(self, tx_gain3):
		"""This return the Transmit amplifier 3. Can be set from -13 dB to 18 dB."""
		return self._tx_gain3
	
	def set_tx_lpf_bandwith(self, tx_lpf_bandwith):
		"""This set a configurable analog filter within the TX path. You may set it to any value in the available list. The values are bandwidths on each side of the center frequencies.
		0 -> 28 MHz
		1 -> 20 MHz
		2 -> 14 MHz
		3 -> 12 MHz
		4 -> 10 MHz
		5 -> 8.75 MHz
		6 -> 7 MHz
		7 -> 6 MHz
		8 -> 5.5 MHz
		9 -> 5 MHz
		10 -> 3.84 MHz
		11 -> 3 MHz
		12 -> 2.75 MHz
		13 -> 2.5 MHz
		14 -> 1.75 MHz
		15 -> 1.5 MHz
		16 -> Bypass"""
		if (tx_lpf_bandwith in range(17)):
			self._tx_lpf_bandwith = tx_lpf_bandwith
		else:
			sys.stderr.write("\nERROR : %s tx_lpf_bandwith must be an integer between 0 and 16 so it can't be %s !\n" % (self._target_id, tx_lpf_bandwith))
			sys.exit(1)		

	def get_tx_lpf_bandwith(self, tx_lpf_bandwith):
		"""This return the configurable analog filter within the TX path. You may set it to any value in the available list. The values are bandwidths on each side of the center frequencies.
		0 -> 28 MHz
		1 -> 20 MHz
		2 -> 14 MHz
		3 -> 12 MHz
		4 -> 10 MHz
		5 -> 8.75 MHz
		6 -> 7 MHz
		7 -> 6 MHz
		8 -> 5.5 MHz
		9 -> 5 MHz
		10 -> 3.84 MHz
		11 -> 3 MHz
		12 -> 2.75 MHz
		13 -> 2.5 MHz
		14 -> 1.75 MHz
		15 -> 1.5 MHz
		16 -> Bypass"""
		return self._tx_lpf_bandwith



class rtdex_source(gr.hier_block2):
	def __init__(self, target_id, packet_size=8192, number_channel=1, channels = "1"):
		gr.hier_block2.__init__(self, "rtdex_source",
                                gr.io_signature(0,0,0),
                                gr.io_signature(1,1,gr.sizeof_gr_complex))


		self._target_id = target_id
		self._packet_size = packet_size
		self._number_channel = number_channel
		self._channels = channels

		self.source = nutaq.rtdex_source(self._target_id,gr.sizeof_short,self._number_channel,3)
		self.source.set_type(0)
		self.source.set_packet_size(self._packet_size)
		self.source.set_channels(self._channels)

		self.blocks_short_to_float_0_0 = blocks.short_to_float(1, 2047)
		self.blocks_short_to_float_0 = blocks.short_to_float(1, 2047)
		self.blocks_float_to_complex_0 = blocks.float_to_complex(1)
		self.blocks_deinterleave_0 = blocks.deinterleave(gr.sizeof_short*1, 1)

		self.connect((self.blocks_deinterleave_0, 0), (self.blocks_short_to_float_0, 0))    
		self.connect((self.blocks_deinterleave_0, 1), (self.blocks_short_to_float_0_0, 0))    
		self.connect((self.blocks_short_to_float_0, 0), (self.blocks_float_to_complex_0, 0))    
		self.connect((self.blocks_short_to_float_0_0, 0), (self.blocks_float_to_complex_0, 1))    
		self.connect((self.source, 0), (self.blocks_deinterleave_0, 0))    

		self.connect(self.blocks_float_to_complex_0, self)


class rtdex_sink(gr.hier_block2):
	def __init__(self, target_id, packet_size=8192, number_channel=1, channels = "1"):
		gr.hier_block2.__init__(self, "rtdex_sink",
                                gr.io_signature(1,1,gr.sizeof_gr_complex),
                                gr.io_signature(0,0,0),)


		self._target_id = target_id
		self._packet_size = packet_size
		self._number_channel = number_channel
		self._channels = channels

		self.sink = nutaq.rtdex_sink(self._target_id,gr.sizeof_short,self._number_channel,3)
		self.sink.set_type(0)
		self.sink.set_packet_size(self._packet_size)
		self.sink.set_channels(self._channels)

		self.blocks_interleave_0 = blocks.interleave(gr.sizeof_short*1, 1)
		self.blocks_float_to_short_0_0_0 = blocks.float_to_short(1, 2**11-1)
		self.blocks_float_to_short_0_0 = blocks.float_to_short(1, 2**11-1)
		self.blocks_complex_to_float_0 = blocks.complex_to_float(1)

		self.connect((self.blocks_complex_to_float_0, 0), (self.blocks_float_to_short_0_0, 0))    
		self.connect((self.blocks_complex_to_float_0, 1), (self.blocks_float_to_short_0_0_0, 0))    
		self.connect((self.blocks_float_to_short_0_0, 0), (self.blocks_interleave_0, 0))    
		self.connect((self.blocks_float_to_short_0_0_0, 0), (self.blocks_interleave_0, 1))    
		self.connect((self.blocks_interleave_0, 0), (self.sink, 0))       

		self.connect(self,self.blocks_complex_to_float_0)
