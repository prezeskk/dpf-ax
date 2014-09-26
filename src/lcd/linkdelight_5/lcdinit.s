	.include 'dpf.inc'

	.area LCDAUX (CODE)

_lcd_custom_init::
	mov	p3dir,#0x0
	anl	p1dir,#0xe8
	anl	p2dir,#0xfd
	orl	wdtcon,#0x20
	clr	LCD_CS
	clr	LCD_RST
	mov	a,#0x96
	lcall	X154a
	setb	LCD_RST
	mov	a,#0x96
	lcall	X154a
	mov	dptr,#_custom_initseq
	ljmp	_lcd_init_by_table
;
X154a:	mov	r5,a
X154b:	mov	r6,#0x18
X154d:	mov	r7,#0xfa
X154f:	djnz	r7,X154f
	djnz	r6,X154d
	djnz	r5,X154b
	ret	
;
_lcd_custom_setcontrast::
	ljmp	_lcd_set_contrast_by_table
;
	.area LCDAUX (CODE)
;        
_custom_contrasttbl::
  .db  0x10, 0x10, 0x10, 0x10, 0x10, 0x10, 0x10
_custom_contrasttbl_len::  .db  7

_custom_contrasttbl2::
  .db  0x71, 0x00, 0x71, 0x00, 0x91, 0x00, 0x91, 0x00, 0xff
_custom_contrasttbl2_len::  .db  9

_custom_contrasttbl2_offsets::
  .db  0x07
_custom_contrasttbl2_offsets_len::  .db  1

_custom_backlighttbl::
  .db  0x00, 0x0a, 0x0b, 0x0c, 0x0d, 0x0e, 0x0f, 0x10, 0x11, 0x12
  .db  0x13, 0x14, 0x15, 0x17, 0x1b, 0x1f, 0x23, 0x27, 0x46, 0x50
  .db  0x6e, 0x78
_custom_backlighttbl_len::  .db  22

_custom_backlighttbl2::
  .db  0x00, 0x03, 0x06, 0x07, 0x08, 0x09, 0x0a, 0x0a, 0x0b, 0x0b
  .db  0x0c, 0x0c, 0x0d, 0x0d, 0x0f, 0x11, 0x13, 0x15, 0x23, 0x28
  .db  0x2d, 0x4a
_custom_backlighttbl2_len::  .db  22

_custom_initseq::
  .db  0x71, 0xef, 0x93, 0x03, 0x80, 0x02, 0x71, 0xcf, 0x93, 0x00
  .db  0x81, 0x30, 0x71, 0xed, 0x94, 0x64, 0x03, 0x12, 0x81, 0x71
  .db  0xe8, 0x93, 0x85, 0x00, 0x78, 0x71, 0xcb, 0x95, 0x39, 0x2c
  .db  0x00, 0x34, 0x02, 0x71, 0xf7, 0x91, 0x20, 0x71, 0xea, 0x92
  .db  0x00, 0x00, 0x71, 0xe8, 0x93, 0x85, 0x0a, 0x78, 0x71, 0x3a
  .db  0x91, 0x55, 0x71, 0x36, 0x91, 0x68, 0x71, 0xc0, 0x91, 0x1d
  .db  0x71, 0xc1, 0x91, 0x12, 0x71, 0xc2, 0x91, 0x22, 0x71, 0xc5
  .db  0x92, 0x35, 0x3c, 0x71, 0xc7, 0x91, 0x97, 0x71, 0xb1, 0x92
  .db  0x00, 0x15, 0x71, 0xb4, 0x91, 0x06, 0x71, 0xb6, 0x92, 0x0a
  .db  0xa2, 0x71, 0xf2, 0x91, 0x00, 0x71, 0x26, 0x91, 0x01, 0x71
  .db  0xe0, 0x9f, 0x0f, 0x22, 0x1c, 0x1b, 0x08, 0x0f, 0x48, 0xb8
  .db  0x34, 0x05, 0x0c, 0x09, 0x0f, 0x07, 0x00, 0x71, 0xe1, 0x9f
  .db  0x00, 0x23, 0x24, 0x07, 0x10, 0x07, 0x38, 0x47, 0x4b, 0x0a
  .db  0x13, 0x06, 0x30, 0x38, 0x0f, 0x71, 0x11, 0x71, 0x29, 0xff
_custom_initseq_len::  .db  140
