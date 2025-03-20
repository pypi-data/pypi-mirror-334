# XLang

## 1. 简介

XLang（X Lang）是一种轻量级、动态类型的脚本语言，结合了函数式和面向对象编程范式的特点。它的设计目标是提供最简单抽象的语法去实现最复杂的功能。XLang 采用基于栈的虚拟机架构执行中间表示代码，适用于快速原型开发、脚本自动化和通用编程任务。

## 2. 语法基础

### 2.1 程序结构

XLang 程序由一系列语句组成，每条语句以分号 `;` 结尾。代码块使用花括号 `{}` 包围。分号分隔的表达式序列会返回最后一个表达式的值，空表达式默认返回 `null`。

```
// 单行注释以双斜杠开头
statement1;
statement2;

/* 
  多行注释使用斜杠星号
  可以跨越多行
*/

{
    // 代码块
    statement3;
    statement4;
}

// 表达式序列返回最后一个表达式的值
result := (a = 1; b = 2; a + b);  // result 的值为 3
```

### 2.2 标识符与关键字

标识符用于命名变量和函数，由字母、数字和下划线组成，但不能以数字开头。XLang 的关键字包括：

- `if`, `else`, `while`, `break`, `continue`, `return`
- `true`, `false`, `null`
- `copy`, `ref`, `deref`, `keyof`, `valueof`, `selfof`, `assert`, `import`
- `self`

## 3. 数据类型

XLang 提供以下数据类型：

### 3.1 基本类型

#### 整数 (Int)

```
x := 42;
```

#### 浮点数 (Float)

```
y := 3.14;
```

#### 字符串 (String)

XLang 支持多种字符串表示形式：单引号、双引号、三引号，并支持字符串转义序列。

```
name1 := "XLang";
name2 := 'XLang';
multiline := '''
  多行
  字符串
''';
```

#### 布尔值 (Bool)

```
isValid := true;
```

#### 空值 (NoneType)

```
data := null;
```

### 3.2 复合类型

#### 元组 (Tuple)

元组是值的有序集合，可包含不同类型：

```
coordinates := (10, 20, 30);
```

#### 键值对 (KeyValue)

键值对用于关联键和值：

```
point := ('x': 10, 'y': 20);
```

#### 函数 (Lambda)

```
adder := (a, b) -> {
    return a + b;
};
```

#### 命名参数 (Named)

```
namedArg := name => "default";
```

#### 内置函数 (BuiltIn)

系统提供的内置函数类型。

## 4. 变量

### 4.1 变量声明和赋值

使用 `:=` 声明新变量，使用 `=` 为已声明变量赋值：

```
// 变量声明
age := 25;

// 变量赋值
age = 26;
```

### 4.2 作用域

XLang 使用动态作用域规则，但**闭包变量需要在参数声明中显式捕获**：

```
x := 10;
{
    // 新的作用域
    y := 20;  // 只在本作用域内有效
    x = 15;   // 可访问并修改外部作用域的变量
}
// y 在此处不可访问
// x 在此处值为 15

// 闭包必须显式捕获外部变量
outer := 100;
func := (captured => outer) -> {  // 显式捕获outer变量
    return captured + 1;
};
```

**注意**：XLang 允许访问调用者的作用域！

## 5. 运算符

### 5.1 运算符优先级

根据AST解析器代码分析，XLang的运算符优先级从高到低排列如下：

1. **最高优先级**

   - 变量/常量/括号表达式/作用域 (优先级1)
   - 成员访问：`.`, `[]`, `()`（函数调用）(优先级2)
   - 修饰符：`copy`, `ref`, `deref`, `keyof`, `valueof`, `selfof`, `assert`, `import` (优先级3)
2. **算术运算符**

   - 乘法级：`*`, `/`, `%` (优先级9)
   - 加法级：`+`, `-` (优先级10)
   - 一元运算符：`+`, `-` (与加法级相同)
3. **比较运算符**

   - 比较级：`>`, `<`, `>=`, `<=`, `==`, `!=` (优先级11)
4. **逻辑运算符**

   - 逻辑级：`not` (优先级12)
   - 逻辑与：`and` (优先级13)
   - 逻辑或：`or` (优先级14)
5. **控制结构**

   - `break`, `continue` (优先级19)
   - `if` (优先级20)
   - `while` (优先级21)
6. **其他运算符**

   - 键值对：`:` (优先级22)
   - 命名参数：`=>` (优先级23)
   - 赋值：`=` (优先级30)
   - 变量声明：`:=` (优先级40)
   - 函数定义：`->` (优先级4)
   - 元组：`,` (优先级59)
   - `return` (优先级60)
   - 语句分隔：`;` (优先级70)

### 5.2 算术运算符

- `+`: 加法
- `-`: 减法
- `*`: 乘法
- `/`: 除法
- `%`: 取模

```
sum := 5 + 3;
difference := 10 - 4;
product := 6 * 7;
quotient := 20 / 4;
remainder := 10 % 3;
```

### 5.3 比较运算符

- `==`: 相等
- `!=`: 不相等
- `<`: 小于
- `>`: 大于
- `<=`: 小于等于
- `>=`: 大于等于

```
isEqual := x == y;
isGreater := age > 18;
```

### 5.4 逻辑运算符

- `not`: 逻辑非
- `and`: 逻辑与
- `or`: 逻辑或

```
isValid := age > 18 and hasID;
isEligible := hasLicense or hasPermit;
```

### 5.5 成员访问运算符

- `.`: 属性访问
- `[]`: 索引访问
- `()`: 函数调用

```
person := ('name': "John", 'age': 30);
personName := person.name;  // 自动将name视为'name'字符串进行属性访问
firstChar := name[0];
result := func(arg);  // 函数调用
```

## 6. 控制结构

### 6.1 条件语句

XLang 支持两种条件语句形式：

```
// 块形式
if condition { // condition为单个token或者被括号包围的表达式
    // 条件为真时执行
} else {
    // 条件为假时执行
};

// 表达式形式
result := if condition 1 else 0;
```

支持 else if 组合：

```
if (operator == "+") {
    // 加法操作
} else if (operator == "-") {
    // 减法操作
} else if (operator == "*") {
    // 乘法操作
} else {
    // 默认操作
};
```

### 6.2 循环语句

```
while condition { // condition为单个token或者被括号包围的表达式
    // 条件为真时重复执行
};
```

### 6.3 中断语句

```
while (condition) {
    if (breakCondition) {
        break;  // 跳出循环
    };
  
    if (skipCondition) {
        continue;  // 跳到下一次迭代
    };
};
```

XLang 的 `break` 和 `continue` 可以穿透内部作用域，直接控制最近的循环：

```
while (i < 5) {
    {
        // 内部作用域
        if (condition) {
            break;  // 跳出外层while循环
        };
    };
    i = i + 1;
};
```

## 7. 函数

### 7.1 函数定义

```
add := (a => 0, b => 0) -> {
    return a + b;
};
```

### 7.2 函数调用

```
result := add(5, 3);
```

### 7.3 默认参数和命名参数

XLang **严格要求**使用 `=>` 操作符声明命名参数：

```
greet := (name => "World", greeting => "Hello") -> {
    return greeting + ", " + name + "!";
};

result1 := greet();  // 使用默认参数
result2 := greet(greeting => "Hi", name => "Alice");  // 使用命名参数
```

### 7.4 闭包与变量捕获

XLang 中的闭包必须**显式捕获**外部变量作为参数：

```
createCounter := (startValue => 0) -> {
    return (count => startValue) -> {  // 显式捕获startValue
        count = count + 1;
        return count;
    };
};

counter := createCounter(10);
value1 := counter();  // 11
value2 := counter();  // 12
```

### 7.5 自引用与方法

通过 `self` 关键字实现对对象自身的引用：

```
person := (
    'name': "John",
    greet => () -> {
        return "Hello, my name is " + self.name;
    }
);
```

**重要特性**：方法可以单独提取并调用，仍然保持对原始对象的引用：

```
method := person.greet;
greeting := method();  // "Hello, my name is John"
```

## 8. 数据结构操作

### 8.1 元组操作

```
// 创建元组
numbers := (1, 2, 3, 4, 5);

// 获取长度
length := len(numbers);

// 索引访问
first := numbers[0];

// 切片
subset := slice(numbers, 1, 3);  // (2, 3)

// 合并元组
combined := numbers + (6, 7, 8);
```

**注意**：元组在构建时会遍历所有元素，如果元素Named下的Lambda类型，会将元组自身引用传递给Lambda的self属性，这样Lambda就可以访问元组的成员。

### 8.2 对象式操作

XLang 使用键值对创建类似对象的结构：

```
// 创建对象
person := (
    'name': "John",
    'age': 30,
    greet => () -> {
        return "Hello, my name is " + self.name;
    }
);

// 访问属性
name := person.name;  // 注意：这里name会被自动解析为'name'字符串

// 调用方法
greeting := person.greet();
```

## 9. 特殊操作符

### 9.1 引用与解引用

```
// 创建引用
x := 10;
xRef := ref x;

// 解引用
deref xRef = 20;  // 修改引用指向的值

// x 的值现在是 20
```

### 9.2 值操作符

```
// 键值操作
obj := ('a': 1, 'b': 2);
keys := keyof obj;    // 获取所有键
values := valueof obj;  // 获取所有值

// 自引用操作
self := selfof func;  // 获取函数的 self 对象

// 复制操作
copied := copy obj;   // 创建深拷贝
```

### 9.3 断言

```
assert(x > 0);  // 如果条件为假，抛出错误
```

## 10. 模块系统

### 10.1 导入模块

XLang 中模块是以特殊格式存储的 IR 代码，使用 `import` 关键字导入：

```
// 导入模块并传递默认参数
// 注意：import返回一个lambda函数，需要调用它获取实际模块内容
mathModule := import "path/to/module.xir" => (config => defaultConfig);

// 调用模块获取实际值
math := mathModule();

// 使用模块功能
result := math.add(5, 3);
```

### 10.2 创建模块

模块实际上是返回对象的代码：

```
// 在module.xir文件中
print(config);  // 使用导入时传入的参数
(
    add => (a => 0, b => 0) -> {
        return a + b;
    },
    subtract => (a => 0, b => 0) -> {
        return a - b;
    }
)
```

## 11. 内置函数

XLang 提供以下内置函数：

### 11.1 输入输出

- `print(...args)`: 输出参数值
- `input()`: 读取用户输入

### 11.2 类型操作

- `type(value)`: 返回值的类型名称
- `int(value)`: 转换为整数
- `float(value)`: 转换为浮点数
- `str(value)`: 转换为字符串
- `bool(value)`: 转换为布尔值
- `repr(value)`: 返回值的详细字符串表示

### 11.3 集合操作

- `len(collection)`: 返回集合长度
- `range(start, end, step)`: 创建数字序列
- `sum(collection)`: 计算集合元素之和
- `max(collection)`: 返回集合中最大元素
- `min(collection)`: 返回集合中最小元素
- `slice(collection, start, end)`: 返回子集合
- `del(collection, index)`: 删除集合中的元素
- `replace(collection, key, value)`: 替换集合中的元素

## 12. 高级功能

### 12.1 迭代器模式

XLang 运行迭代语法，但同样可以实现迭代器模式：

```
iterator := (
    iter => (container => ('T' : null), n => 0) -> {
        n = n + 1;
        E := valueof container;  // 获取容器的值引用
        T := keyof container;    // 获取容器的键
        if (n <= len(T)) {
            (deref E) = T[n - 1];  // 更新引用值
            return true;
        } else {
            return false;
        };
    },
    loop => (func => (n => 0) -> {return false}) -> {
        return (n => 0, func => func) -> {
            while (func(n)) {
                n = n + 1;
            };
        };
    }
);

// 使用迭代器
loop_func := iterator.loop((n => 0) -> {
    print(n);
    return n < 5;  // 继续条件
});

loop_func();  // 执行迭代
```

### 12.2 函数式编程

XLang 支持高阶函数和函数式编程范式：

```
// Z组合子实现匿名递归函数
Z := (f => (x => null) -> { return x(x); }) -> {
    return f((x => null, f => f) -> {
        return f(Z(f))(x);
    });
};

// 使用Z组合子实现阶乘函数
factorial := Z((f => null) -> {
    return (n => 0, f => f) -> {
        if (n <= 1) {
            return 1;
        } else {
            return n * f(n - 1);
        };
    };
});

print(factorial(5));  // 120
```

## 13. 示例代码

### 13.1 简单函数

```
add := (a => 0, b => 0) -> {
    return a + b;
};
print(add(5, 3));  // 输出: 8
```

### 13.2 对象和方法

```
person := (
    'name': 'Alice',
    greet => (message => 'Hello') -> {
        return message + ", " + self.name + "!";
    }
);
print(person.greet());  // 输出: Hello, Alice!

method := person.greet;
print(method());  // 仍然输出: Hello, Alice!
```

### 13.3 闭包和状态

```
createCounter := () -> {
    count := 0;
    return (count => count) -> { // 返回闭包，显式捕获count
        count = count + 1;
        return count;
    };
};

counter := createCounter();
print(counter());  // 输出: 1
print(counter());  // 输出: 2
```

### 13.4 条件表达式

```
max := (a, b) -> {
    return if a > b a else b;
};

print(max(5, 3));  // 输出: 5
```

### 13.5 复杂对象操作

```
// 创建一个"类"
Person := (name => '', age => 0) -> {
    return (
        'name': name,
        'age': age,
        greet => () -> {
            return "Hello, I'm " + self.name;
        },
        birthday => () -> {
            self.age = self.age + 1;
            return "Happy birthday! Now I'm " + str(self.age);
        }
    );
};

// 创建实例
john := Person("John", 30);
greeting := john.greet();
birthday_message := john.birthday();
```

### 13.6 复杂表达式的优先级示例

```
// 算术运算符优先级
result := 2 + 3 * 4;  // 等于 2 + (3 * 4) = 14

// 成员访问优先级高于其他操作符
obj := ('value': 5, 'multiplier': 2);
result := obj.value * obj.multiplier;  // 10

// 函数调用优先级与成员访问相同
add := (a, b) -> { return a + b; };
result := add(2, 3) * 4;  // (2+3) * 4 = 20

// 赋值优先级低于大多数操作
x := 0;
x = 1 + 2;  // x = (1+2) = 3

// 逻辑运算符优先级
condition := 5 > 3 and 10 < 20;  // (5 > 3) and (10 < 20) = true
```

## 14. 错误处理

XLang 使用异常进行错误处理，运行时错误会导致程序终止并提供详细的错误信息：

- 代码位置 (行号和列号)
- 错误类型和消息
- 调用堆栈追踪
- 相关代码段

使用 `assert` 可以进行条件检查：

```
// 断言条件为真，否则抛出错误
assert(x > 0);
```

## 15. 最佳实践

1. **显式变量捕获**

   ```
   outer := 10;
   // 正确：显式捕获外部变量
   func := (captured => outer) -> { return captured + 1; };
   ```
2. **使用命名参数提高可读性**

   ```
   createPerson(name => "John", age => 30);
   ```
3. **使用元组实现面向对象编程**

   ```
   person := (
       'name': "John",
       greet => () -> { return "Hello, " + self.name; }
   );
   ```
4. **模块化代码**

   ```
   // 创建可复用的模块
   mathModule := (
       add => (a => 0, b => 0) -> { return a + b; },
       multiply => (a => 0, b => 0) -> { return a * b; }
   );
   ```
5. **使用引用类型管理共享状态**

   ```
   shared := ('count': 0);
   sharedRef := ref shared;
   ```
6. **使用分号分隔表达式序列**

   ```
   // 多个表达式，返回最后一个表达式的值
   result := (x = 1; y = 2; x + y);  // result为3
   ```
7. **合理运用运算符优先级**

   ```
   // 使用括号明确优先级
   result := (1 + 2) * 3;  // 而不是依赖默认优先级
   ```

## 16. 局限性与注意事项

1. **闭包变量必须显式捕获**：所有在闭包中使用的外部变量必须作为参数显式捕获。
2. **分号要求**：所有表达式末尾必须有分号（除了最后一个表达式），包括控制结构。
3. **动态类型检查**：类型错误在运行时检测，没有静态类型检查。
4. **条件表达式括号**：块形式的 `if`和 `while`语句的条件如果是复杂表达式必须用括号包围。
5. **模块导入机制**：模块被视为Lambda表达式，必须先调用才能获取实际内容。
6. **属性访问自动转换**：当使用点操作符访问对象属性时，如 `obj.name`，标识符 `name`会被自动解析为字符串 `'name'`。
7. **表达式序列**：分号分隔的表达式序列会返回最后一个表达式的值，空表达式返回 `null`。
8. **运算符优先级**：注意运算符的优先级顺序，特别是在复杂表达式中，必要时使用括号明确意图。
9. **参数缓存**：Lambda函数的参数会被缓存，也就是说，如果不显示指定参数的值，那么参数会使用上一次的值。
10. **元组Lambda捕获**：元组在构建时会遍历所有元素，如果元素是Named类型的值且值是Lambda类型，会将元组自身引用传递给Lambda的self属性，这样Lambda就可以访问元组的成员。
