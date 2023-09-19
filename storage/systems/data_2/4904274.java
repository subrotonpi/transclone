) public static void main ( String n , String x ) {
  int [ ] a = new int [ n ] ;
  for ( int i = 0 ;
  i < n ;
  i ++ ) a [ i ] = Integer . parseInt ( x ) ;
  int price = 0 ;
  String s = Integer . toBinaryString ( x ) ;
  for ( int i = s . length ( ) - 1 ;
  i >= 0 ;
  i -- ) {
    if ( s . charAt ( s . length ( ) - 1 - i ) == "1" ) {
      price += a [ i ] ;
    }
  }
  System . out . println ( price ) ;
}
