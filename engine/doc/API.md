# API Reference

> last update in 2023/2/10 by Tianyi Huang

### Game Memory API

service to provide control on player's game memory

**get all memory slot:** 

+ `description`: return all memory that player saved

+ `api`: /get_all_memory
+ `method`: GET
+ `request format`: \

```json

```

+ `request`: \
+ `return format`: json
+ `return description`: return a json list that the key is the time that the player create such memory, and value is the frame number (current progress)

```json
[
    "1676053769.6973011": 12,
    "1676053769.6993163": 13
]
```

**dump memory:**

+ `description`: localize player's progress

+ `api`: /set_memory
+ `method`: POST
+ `request format`: json
+ `request`: "progress": [frame number]

```json
"progress": 12 
```

+ `return format`: str
+ `return description`: return a string which represent the create time of such memory

```json
"1676053769.6973011"
```

**remove memory:**

+ `description`: remove gamer' s specific memory from slot

+ `api`: /remove_memory
+ `method`: POST
+ `request format`: json
+ `request`: "time_create": [memory create time]

```json
"time_create": "1676053769.6973011"
```

+ `return format`: str
+ `return description`: return a string which represent the create time of such memory, or -1 when remove unsuccessfully 

```json
"1676053769.6973011"
```

**reset slot:**

+ `description`: initialize the whole memory slot, this action will destroy all memory

+ `api`: /reset_slot
+ `method`: POST
+ `request format`: \
+ `request`: \

```json

```

+ `return format`: int
+ `return description`: return `1` if successfully reset or -1 otherwise   

```json
1
```

