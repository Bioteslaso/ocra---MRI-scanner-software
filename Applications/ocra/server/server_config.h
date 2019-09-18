#ifndef _SERVER_CONFIG_H
#define _SERVER_CONFIG_H

#include <stdint.h>

// Memory map
static const uint32_t SLCR_OFFSET = 0xf8000000,
	CFG_OFFSET = 0x40000000,
	STS_OFFSET = 0x40001000,
	RX_DATA_OFFSET = 0x40080000,
	TX_DATA_OFFSET = 0x40020000,
	PULSEQ_MEMORY_OFFSET = 0x40070000,
	SEQ_CONFIG_OFFSET = 0x40080000,
	GRADIENT_MEMORY_X_OFFSET = 0x400a0000,
	GRADIENT_MEMORY_Y_OFFSET = 0x400b0000,
	GRADIENT_MEMORY_Z_OFFSET = 0x400c0000;

// FPGA clock frequency (HZ)
static const double FPGA_CLK_FREQ_HZ = 122.88e6;

#endif