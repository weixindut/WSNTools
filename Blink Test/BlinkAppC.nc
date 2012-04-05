// $Id: BlinkAppC.nc,v 1.5 2009/10/26 07:34:10 vlahan Exp $

configuration BlinkAppC
{
}
implementation
{
  components MainC, BlinkC, LedsC,RpcC,RamSymbolsM;
////  components new TimerMilliC() as Timer0;


  BlinkC -> MainC.Boot;

////  BlinkC.Timer0 -> Timer0;
  BlinkC.Leds -> LedsC;
  BlinkC.SplitControl -> RpcC;
}

