interface xinxin 
{
  command error_t xinxinCommand(uint8_t data);
  event void xinxinEvent();
  event RpcCommandMsg xinxinEvent2(RpcCommandMsg data);
}
