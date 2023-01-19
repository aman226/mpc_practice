#include "stdint.h"
#define PITCH_LOOKUP_LENGTH 7
#define YAW_LOOKUP_LENGTH 7
#define THROTTLE_LOOKUP_LENGTH 12

typedef struct controlRateConfig_s {
        uint8_t rcRate8;
        uint8_t rcExpo8;
        uint8_t thrMid8;
        uint8_t thrExpo8;
        uint8_t rates[3];
        uint8_t dynThrPID;
        uint8_t rcYawExpo8;
        uint16_t tpa_breakpoint;                // Breakpoint where TPA is activated
} controlRateConfig_t;

typedef struct escAndServoConfig_s {
        // PWM values, in milliseconds, common range is 1000-2000 (1 to 2ms)
        uint16_t minthrottle; // Set the minimum throttle command sent to the ESC (Electronic Speed Controller). This is the minimum value that allow motors to run at a idle speed.
        uint16_t maxthrottle; // This is the maximum value for the ESCs at full power this value can be increased up to 2000
        uint16_t mincommand; // This is the value for the ESCs when they are not armed. In some cases, this value must be lowered down to 900 for some specific ESCs
        uint16_t servoCenterPulse;         // This is the value for servos when they should be in the middle. e.g. 1500.
} escAndServoConfig_t;

int16_t lookupPitchRollRC[PITCH_LOOKUP_LENGTH];     // lookup table for expo & RC rate PITCH+ROLL
int16_t lookupYawRC[YAW_LOOKUP_LENGTH];     // lookup table for expo & RC rate YAW
int16_t lookupThrottleRC[THROTTLE_LOOKUP_LENGTH];   // lookup table for expo & mid THROTTLE

void generatePitchRollCurve(controlRateConfig_t *controlRateConfig)
{
    uint8_t i;

    for (i = 0; i < PITCH_LOOKUP_LENGTH; i++)
        lookupPitchRollRC[i] = (2500 + controlRateConfig->rcExpo8 * (i * i - 25)) * i * (int32_t) controlRateConfig->rcRate8 / 2500;
}

void generateYawCurve(controlRateConfig_t *controlRateConfig)
{
    uint8_t i;

    for (i = 0; i < YAW_LOOKUP_LENGTH; i++)
        lookupYawRC[i] = (2500 + controlRateConfig->rcYawExpo8 * (i * i - 25)) * i / 25;
}

void generateThrottleCurve(controlRateConfig_t *controlRateConfig, escAndServoConfig_t *escAndServoConfig)
{
    uint8_t i;

    for (i = 0; i < THROTTLE_LOOKUP_LENGTH; i++) {
        int16_t tmp = 10 * i - controlRateConfig->thrMid8;
        uint8_t y = 1;
        if (tmp > 0)
            y = 100 - controlRateConfig->thrMid8;
        if (tmp < 0)
            y = controlRateConfig->thrMid8;
        lookupThrottleRC[i] = 10 * controlRateConfig->thrMid8 + tmp * (100 - controlRateConfig->thrExpo8 + (int32_t) controlRateConfig->thrExpo8 * (tmp * tmp) / (y * y)) / 10;
        lookupThrottleRC[i] = escAndServoConfig->minthrottle + (int32_t) (escAndServoConfig->maxthrottle - escAndServoConfig->minthrottle) * lookupThrottleRC[i] / 1000; // [MINTHROTTLE;MAXTHROTTLE]
    }
}