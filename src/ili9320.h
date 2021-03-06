/**************************************************************************
 * Definitions for the ILI9320 LCD controller
 *
 * This file was generated by dclib/netpp. Modifications to this file will
 * be lost.
 * Stylesheet: reg8051.xsl       (c) 2010-2011 section5
 *
 * Version: 0.0develop
 **************************************************************************/



#ifndef _BITMASK_
#define _BITMASK_(msb, lsb) ( (-1 << (msb + 1)) ^ (-1 << lsb) )
#endif
#ifndef _BIT_
#define _BIT_(pos) (1 << pos)
#endif



/*********************************************************
 * Address segment 'LCD'
 *********************************************************/
		
#define R_LCD_StartOsc             0x00
#	define OSC         _BIT_(0)
#define R_LCD_DrvOutCtrl           0x01
#	define SM          _BIT_(10)
#	define SS          _BIT_(8)
#define R_LCD_LCDDrvWaveformCtrl   0x02
#define R_LCD_EntryMode            0x03
#	define BGR         _BIT_(12)
#	define ORG         _BIT_(7)
#	define INC_V       _BIT_(5)     // Vertical: 0: dec, 1: increment
#	define INC_H       _BIT_(4)     // Horizontal: 0: dec, 1: increment
#	define AM_V        _BIT_(3)     // Control GRAM update direction, 0: Horizontal, 1: Vertical
#define R_LCD_ScalingCtrl          0x04
#define R_LCD_DispCtrl1            0x07
#define R_LCD_DispCtrl2            0x08
#define R_LCD_DispCtrl3            0x09
#define R_LCD_FrameCycleCtrl       0x0a
#define R_LCD_ExDispInterfCtrl1    0x0c
#define R_LCD_FrameMakerPos        0x0d
#define R_LCD_ExDispInterfCtrl2    0x0f
#define R_LCD_PowerCtrl1           0x10
#define R_LCD_PowerCtrl2           0x11
#define R_LCD_PowerCtrl3           0x12
#define R_LCD_PowerCtrl4           0x13
#define R_LCD_GRAMAddrSetHori      0x20
#define R_LCD_GRAMAddrSetVerti     0x21
#define R_LCD_WriteGRAM            0x22
#define R_LCD_PowerCtrl7           0x29
#define R_LCD_FrameRateCtrl        0x2b
#define R_LCD_GammaCtrl0           0x30
#define R_LCD_GammaCtrl1           0x31
#define R_LCD_GammaCtrl2           0x32
#define R_LCD_GammaCtrl3           0x33
#define R_LCD_GammaCtrl4           0x34
#define R_LCD_GammaCtrl5           0x35
#define R_LCD_GammaCtrl6           0x36
#define R_LCD_GammaCtrl7           0x37
#define R_LCD_GammaCtrl8           0x38
#define R_LCD_GammaCtrl9           0x39
#define R_LCD_GammaCtrl10          0x3a
#define R_LCD_GammaCtrl11          0x3b
#define R_LCD_GammaCtrl12          0x3c
#define R_LCD_GammaCtrl13          0x3d
#define R_LCD_WinAddrHoriStart     0x50
#define R_LCD_WinAddrHoriEnd       0x51
#define R_LCD_WinAddrVertStart     0x52
#define R_LCD_WinAddrVertEnd       0x53
#define R_LCD_DrvOutCtrl1          0x60
#define R_LCD_DrvOutCtrl2          0x61
#define R_LCD_VertScrollCtrl       0x6a
#define R_LCD_DispPosPartial1      0x80
#define R_LCD_RamAddrStartPartial1 0x81
#define R_LCD_RamAddrEndPartial1   0x82
#define R_LCD_DisplayPosPartial2   0x83
#define R_LCD_RamAddrStartPartial2 0x84
#define R_LCD_RamAddrEndPartial2   0x85
#define R_LCD_PanelIfaceCtrl1      0x90
#define R_LCD_PanelIfaceCtrl2      0x92
#define R_LCD_PanelIfaceCtrl3      0x93
#define R_LCD_PanelIfaceCtrl4      0x95
#define R_LCD_PanelIfaceCtrl5      0x97
#define R_LCD_PanelIfaceCtrl6      0x98
