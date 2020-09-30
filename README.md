# Aidon 6534

  
| Aidon RJ12 | USB serial |
| ----       | ----       |
| 1 - 5V     |            |
| 2 - RTS    | 5V         |
| 3 - GND    | GND        |
| 4 -        |            |
| 5 - Data   | RxD        |
| 6 - GND    |            |

## Data Sent

The software sends out to the following MQTT topics:

```
meter/activepower
meter/activepower1
meter/activepower2
meter/activepower3
meter/voltage1
meter/voltage2
meter/voltage3
meter/current1
meter/current2
meter/current3
meter/activeenergy
```

