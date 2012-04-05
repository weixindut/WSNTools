interface tianwei
{
  command void tianweiCommand();
  command RpcCommandMsg tianweiCommand2();
  event error_t tianweiEvent(RpcCommandMsg data);
  command void testCommand7(RpcCommandMsg data);
}
