static final Scanner scanner = new Scanner ( System . in ) {
  @ Override public void next ( ) {
    String l = scanner . nextLine ( ) ;
    int n = Integer . parseInt ( l ) ;
    for ( int i = 0 ;
    i < n ;
    i ++ ) {
      System . out . format ( "Case #%d:" , i + 1 ) ;
      l = scanner . nextLine ( ) ;
      int nEngines = Integer . parseInt ( l ) ;
      List < String > engines = new ArrayList < String > ( ) ;
      for ( int j = 0 ;
      j < nEngines ;
      j ++ ) {
        l = scanner . nextLine ( ) ;
        engines . add ( l . trim ( ) ) ;
      }
      l = scanner . nextLine ( ) ;
      int nSearches = Integer . parseInt ( l ) ;
      List < String > remaining = engines . stream ( ) . collect ( Collectors . toList ( ) ) ;
      int switches = 0 ;
      for ( int j = 0 ;
      j < nSearches ;
      j ++ ) {
        l = scanner . nextLine ( ) ;
        String search = l . trim ( ) ;
        if ( remaining . contains ( search ) ) {
          remaining . remove ( search ) ;
          if ( remaining . isEmpty ( ) ) {
            switches ++ ;
            remaining = engines . stream ( ) . collect ( Collectors . toList ( ) ) ;
            remaining . remove ( search ) ;
          }
        }
      }
      System . out . println ( switches ) ;
    }
  }
}
