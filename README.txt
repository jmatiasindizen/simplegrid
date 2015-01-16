Tiene que haber un modulo de middleware basado en redis:
- Channel
- Data_queue
- Publisher / Subscriber (redis) (NOTIFICACIONES)
- ¿Idem pero para enviar JSON's? Solo Productor / Consumidor. Interesa 
  sobre todo la parte consumidora de los workers la parte productora ya 
  está hecha en el API REST.

¿Como implementar en cada componente del grid la parte que escucha?
- Tarea de escucha. Esta a la espera de las ordenes de su superior.
- Tareas normales. Como hacer

Canales de escucha:
- Broker: 
	* Recibe del monitor las operaciones basicas (Init, Start, Stop, ...)
	* Recibe la politica de orquestación.
	
	
- Worker:
	* Recibe del broker operaciones basicas
	*
