/* LCD brigtness / contrast adjust */

#include "global.h"
#include "dpf.h"
#include "lcd.h"
#include "print.h"
#include "utils.h"

#pragma codeseg LCDAUX
#pragma constseg LCDAUX

#ifdef LCD_BACKLIGHT_HIGH
extern __code unsigned char custom_backlighttbl_len;
extern __code unsigned char custom_backlighttbl[];
extern __code unsigned char custom_backlighttbl2_len;
extern __code unsigned char custom_backlighttbl2[];
#endif

void _set_brightness(BYTE brightness)
{
	unsigned int per;
	unsigned int pwm;

#ifndef LCD_BACKLIGHT_HIGH
	// Clock-gen = RTC, 32,768 kHz
	if (brightness > MAX_BRIGHTNESS_VALUE)
	    brightness = MAX_BRIGHTNESS_VALUE;
	// PWM adjustment
	per = MAX_BRIGHTNESS_VALUE;
	pwm = (MAX_BRIGHTNESS_VALUE - brightness);
#else
	// Clock-gen = sys-clock, 12 / 48 MHz
	if (brightness >= custom_backlighttbl_len)
		brightness = custom_backlighttbl_len - 1;
	if (custom_backlighttbl2_len > 0)
	{
	// FREQ adjustment
		per = custom_backlighttbl[brightness];
		pwm = custom_backlighttbl2[brightness];
	}
	else
	{
	// PWM adjustment
		per = 0x0FF0;
		pwm = 0xFF0 - (custom_backlighttbl[brightness] << 4);
	}
	if (pcon & (2 << TMRCSEL_SHFT)){	// 48 MHz ? 
		per *= 2;
		pwm *= 2;
	} else if ((pcon & TMRCSEL) == (1 << TMRCSEL_SHFT)){	// 12 MHz ? 
		per = ++per / 2;
		pwm = ++pwm / 2;
	}

	tmr1con &= T1ON;
#endif

	//GOTOXY(1, 8); print_short(per); putchar(' '); print_short(pwm);

	tmr1perl = per & 0xFF;
	tmr1perh = per >> 8;
	tmr1pwml = pwm & 0xFF;
	tmr1pwmh = pwm >> 8;

	tmr1cntl = 0;
	tmr1cnth = 0;

#ifdef LCD_BACKLIGHT_HIGH
	tmr1con = T1POS1 | T1POEN | T1ON;
#endif
}

void set_brightness(BYTE brightness) __banked
{
	_set_brightness(brightness);
}
