#!/usr/bin/env python
# -*- coding: utf-8 -*-
# 
# Copyright 2015 <+YOU OR YOUR COMPANY+>.
# 
# This is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3, or (at your option)
# any later version.
# 
# This software is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License
# along with this software; see the file COPYING.  If not, write to
# the Free Software Foundation, Inc., 51 Franklin Street,
# Boston, MA 02110-1301, USA.
# 

# import numpy
from gnuradio import gr
import sys
from scipy import *
from pylab import *
from scipy.io import wavfile
import numpy as np

class autotune(gr.sync_block):
    """
    docstring for block autotune
    """
    def __init__(self, file, chunksize_pow):
        self.file = file
        self.chunksize_pow = chunksize_pow
        gr.sync_block.__init__(self,
            name="autotune",
            in_sig=None,
            out_sig=[np.int32])

    def work(self, input_items, output_items):
        out = output_items[0]
        out=[]
        size = 2**self.chunksize_pow
        # size = 2**15

        samp_rate, inputa = wavfile.read(self.file);
        # <+signal processing here+>
        # out[:] = whatever

        def frequency(sub_array):
            # sub_array = sound_array
            hanning_window = np.hanning(len(sub_array))
            fft = np.fft.fft(hanning_window*sub_array)
            abs_fft = np.abs(fft)
            m = max(abs_fft)
            index = [k for k,j in enumerate(abs_fft) if j==m][0]
            if(index>size/2):index = size-index
            # if(len(sub_array)==size) :print abs_fft[260], abs_fft[16124]
            # if index==0:index = 1
            # print index
            # print m
            # print abs_fft[0]
            return index*samp_rate/size 

        def speedx(sound_array, factor):
            """ Multiplies the sound's speed by some `factor` """
            indices = np.round( np.arange(0, len(sound_array), factor) )
            indices = indices[indices < len(sound_array)].astype(int)
            return sound_array[ indices.astype(int) ]

        def stretch(sound_array, f, window_size, h):
            """ Stretches the sound by a factor `f` """

            phase  = np.zeros(window_size)
            hanning_window = np.hanning(window_size)
            result = np.zeros( len(sound_array) /f)
            # result = np.zeros( len(sound_array) /f + window_size)

            for i in np.arange(0, len(sound_array)-(window_size+h), h*f):

                a1 = sound_array[i: i + window_size]
                a2 = sound_array[i + h: i + window_size + h]
                s1 =  np.fft.fft(hanning_window * a1)
                s2 =  np.fft.fft(hanning_window * a2)
                phase = (phase + np.angle(s2/s1)) % 2*np.pi
                a2_rephased = np.fft.ifft(np.abs(s2)*np.exp(1j*phase))
                i2 = int(i/f)
                result[i2 : i2 + window_size] += hanning_window*a2_rephased
            result = ((2**(14)) * result/result.max()) # normalize (16bit)

            return result.astype('int16')

        for i in xrange(0, len(inputa),size):
            sub_array = inputa[i:i+size]
            f = frequency(sub_array)
            print self.file
            print self.chunksize_pow
            print samp_rate
            print len(inputa)
            n_pitch =12*np.log2(f/440.0)
            n_pitch = np.rint(n_pitch)
            near_frequency = 440.0*np.exp2(n_pitch/12) 
            factor = near_frequency/f
            stretched = stretch(inputa[i:i+size], factor, 2**12, 2**10)
            # outputa[i*size:(i+1)*size] = speedx(stretched[2**12:],1/factor)
            out = np.concatenate([out ,speedx(stretched,1/factor)]).astype(int32)
        # x =True

        # print output_items[0]
        # print len(output_items[0])
        return len(output_items[0])

