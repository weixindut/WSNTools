includes Rpc;
////includes Timer;
//#include "Timer.h"

module BlinkC
{
////  uses interface Timer<TMilli> as Timer0 ;
  uses interface Leds;
  uses interface SplitControl;
  uses interface Boot;

  provides{
	command void initLeds() @rpc();
	command void initLeds2(uint8_t value) @rpc();
////	event void Timer0.fired() @rpc();
	}
}
implementation
{
     uint8_t counter;
  event void Boot.booted()
  {
      call SplitControl.start();		//new add***************
////      call Timer0.startPeriodic( 1000 );
      counter = 1;
    call initLeds();
  }
  command void initLeds()
  {
    call Leds.set(counter);
  }
  command void initLeds2(uint8_t value)
  {
    call Leds.set(value);
  }
////   event void Timer0.fired()
////   {
////      counter++;
////      call Leds.set(counter);
////   }
  
  event void SplitControl.startDone(error_t error){
  }

  event void SplitControl.stopDone(error_t error){
  }
}
