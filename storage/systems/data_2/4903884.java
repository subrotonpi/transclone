public static void a ( String input ) {
  int b = Integer . parseInt ( input ) ;
  List < Integer > hoge = Lists . newArrayList ( ) ;
  hoge . add ( a ) ;
  String c = Integer . toBinaryString ( b ) ;
  c = c . substring ( 2 ) ;
  c = c . substring ( 0 , c . length ( ) - 1 ) ;
  int ans = 0 ;
  for ( int i = 0 ;
  i < c . length ( ) ;
  i ++ ) {
    if ( ( c . charAt ( i ) == '1' ) ) {
      ans += hoge . get ( i ) ;
    }
  }
  System . out . println ( ans ) ;
}
