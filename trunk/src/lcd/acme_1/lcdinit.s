	.include 'dpf.inc'

	.area LCDAUX (CODE)

_lcd_custom_init::
	mov	p3dir,#0x0
	anl	p1dir,#0xe8
	anl	p2dir,#0xfd
	clr	LCD_CS
	clr	LCD_RST
	mov	a,#0x96
	lcall	X1639
	setb	LCD_RST
	mov	a,#0xc8
	lcall	X1639
	mov	a,#0xe2
	lcall	X164f
	mov	a,#0xc8
	lcall	X1639
	mov	a,#0xc8
	lcall	X1639
	mov	a,#0xc8
	lcall	X1639
	mov	a,#0xea
	lcall	X164f
	mov	a,#0x81
	lcall	X164f
	mov	a,#0x84
	lcall	X164f
	mov	a,#0x2f
	lcall	X164f
	mov	a,#0xd1
	lcall	X164f
	mov	a,#0xd6
	lcall	X164f
	mov	a,#0xc0
	lcall	X164f
	mov	a,#0x89
	mov	a,#0xa2
	lcall	X164f
	mov	a,#0xc8
	lcall	X164f
	mov	a,#0x18
	lcall	X164f
	mov	a,#0xde
	lcall	X164f
	mov	a,#0xaf
	lcall	X164f
	ret	
;
X1639:	mov	r5,a
X163a:	mov	r6,#0x18
X163c:	mov	r7,#0xfa
X163e:	djnz	r7,X163e
	djnz	r6,X163c
	djnz	r5,X163a
	ret	
;
X164f:	clr	LCD_A0
	ljmp	otp_lcd_write
;
X1654:	clr	LCD_A0
	ljmp	otp_lcd_write
