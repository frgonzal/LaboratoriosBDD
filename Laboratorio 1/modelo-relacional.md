## Entidades

Jugador(**nick**, nombre, plataforma, )


PC_player(**nick_Pc_player**, jugadorSteam)

- **nick_Pc_player** REF Jugador(**nick**)


Android_player(**nick_android**)

- **nick_android** REF Jugador(**nick**)


Sala(**Código**, cantMax)


Mapa(**nombre**, descripción)    


Juego(**código_sala**, **fecha**, gana_impostor)

- **código_sala** REF Sala(Código)


Mensaje(**nick_jugador**, **fecha**)

- **nick_jugador** REF Jugador(nick_jugador)


## Relaciones


Ocurre_En(**codigo_juego**, nombre_Mapa)

- **codigo_juego** REF Juego(**codigo_sala**)

- nombre_Mapa REF Mapa(**nombre**) 


Creada_Por(**codigo_sala_creada**, nick_player)

- **codigo_sala_creada** REF Sala(**codigo**)

- nick_player  REF Jugador(**nick**)


Pertenece(**nick_player**, **codigo_sala**, fecha_ingreso)

- **nick_player** REF Jugador(**nick**)

- **codigo_sala** REF Sala(**Código**)


Juega(**nick_player**, **código_juego**, Color, Estado_Jugador, Impostor_Secretamente)

- **nick_player** REF Jugador(**nick**)

- **codigo_juego** REF Juego(**codigo_sala**)


Existe_En(**código_sala**, **fecha_juego**)

- **código_sala** REF Sala(**Código**)

- **fecha_juego** REF Juego(**fecha**)


Envía(**nick_jugador**,**Fecha_mensaje**, **código_juego**, **fecha_juego**, mensaje)

- **nick_jugador** REF Jugador(**nick**)

- (**código_juego**, **fecha_juego**) REF Juego(**codigo_sala**, **fecha**)

- (**Fecha_mensaje**, mensaje) REF Mensaje(**Fecha_mensaje**, mensaje)
