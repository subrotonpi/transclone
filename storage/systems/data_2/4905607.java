public static void input ( ) {
  list = input . split ( "\\s+" ) ;
  a = input . split ( "\\s+" ) ;
  int b = Integer . parseInt ( list [ 1 ] ) ;
  int sum = 0 ;
  for ( int i = 0 ;
  i < Integer . parseInt ( list [ 0 ] ) ;
  i ++ ) {
    if ( b % 2 == 1 ) {
      sum += Integer . parseInt ( a [ i ] ) ;
    }
    b = b / 2 ;
  }
  System . out . println ( sum ) ;
}
