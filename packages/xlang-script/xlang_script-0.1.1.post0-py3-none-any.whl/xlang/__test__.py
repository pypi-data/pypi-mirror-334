from .xlang.lang import XLang
import json

def test():
    module = """
    print(A);
    (
        iter => (container => ('T' : null), n => 0) -> {
            n = n + 1;
            E := valueof container;
            T := keyof container;
            if (n <= len(T)) {
                (deref E) = T[n - 1];
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
    )

    """  # 使用最后一个表达式作为返回值或者使用return语句返回值

    code = """
    module := import "modules/test.xir" => (A => "Default Value"); // Import the module as Lambda, () is the default argument
    module := module(); // Call the module to get the actual value
    print(repr(module));

    loop_func := module.loop((n => 0) -> {
        print(n);
        return n < 20;
    });

    loop_func();

"""

    xlang = XLang()
    ir = xlang.compile(module)
    with open("modules/test.xir", "w", encoding='utf-8') as f:
        f.write(json.dumps(ir.export_to_dict(), indent=2, ensure_ascii=False))
    result = xlang.execute(code)
    print(result)


def test_break_continue():
    # 测试代码：测试break和continue在各种嵌套结构中的行为
    code = """
    // 测试1: 简单的break
    i := 0;
    print("测试1: 简单的break");
    while (i < 10) {
        print("i = " + str(i));
        if (i == 5) {
            print("遇到5，跳出循环");
            break;
        };
        i = i + 1;
    };
    print("循环结束，i = " + str(i));
    print("");

    // 测试2: 简单的continue
    i = 0;
    print("测试2: 简单的continue");
    while (i < 10) {
        i = i + 1;
        if (i % 2 == 0) {
            print("跳过偶数: " + str(i));
            continue;
        };
        print("处理奇数: " + str(i));
    };
    print("");

    // 测试3: 带作用域的break
    i = 0;
    print("测试3: 带作用域的break");
    while (i < 5) {
        {
            // 创建一个新的作用域
            j := 100 + i;
            print("新作用域, j = " + str(j));
            if (i == 3) {
                print("遇到i=3，从内层作用域break");
                break;
            };
        };
        i = i + 1;
    };
    print("循环结束，i = " + str(i));
    print("");

    // 测试4: 带作用域的continue
    i = 0;
    print("测试4: 带作用域的continue");
    while (i < 5) {
        i = i + 1;
        {
            // 创建一个新的作用域
            j := 100 + i;
            print("新作用域, i = " + str(i) + ", j = " + str(j));
            if (i == 2) {
                print("遇到i=2，从内层作用域continue");
                continue;
            };
            print("增加i后，i = " + str(i));

        };
    };
    print("");

    // 测试5: 嵌套循环中的break
    print("测试5: 嵌套循环中的break");
    i = 0;
    while (i < 3) {
        print("外层循环: i = " + str(i));
        j := 0;
        while (j < 3) {
            print("  内层循环: j = " + str(j));
            if (j == 1) {
                print("  遇到j=1，跳出内层循环");
                break;
            };
            j = j + 1;
        };
        i = i + 1;
    };
    print("");

    // 测试6: 嵌套循环中的continue
    print("测试6: 嵌套循环中的continue");
    i = 0;
    while (i < 3) {
        print("外层循环: i = " + str(i));
        j := 0;
        while (j < 3) {
            j = j + 1;
            if (j == 2) {
                print("  跳过j=2");
                continue;
            };
            print("  内层循环: j = " + str(j));
        };
        i = i + 1;
    };
    print("");

    // 测试7: 复杂嵌套结构中的break和continue
    print("测试7: 复杂嵌套结构中的break和continue");
    i = 0;
    while (i < 5) {
        print("外层循环: i = " + str(i));
        if (i == 0) {
            i = i + 1;
            print("i=0时continue");
            continue;
        };
        if (i == 4) {
            print("i=4时break");
            break;
        };
        {
            // 嵌套作用域
            j := 0;
            while (j < 3) {
                {
                    // 更深层的嵌套作用域
                    k := i * 10 + j;
                    print("  深层嵌套: i=" + str(i) + ", j=" + str(j) + ", k=" + str(k));
                    if (k > 20) {
                        print("  k>20，跳出内层循环");
                        break;
                    };
                };
                j = j + 1;
            };
        };
        i = i + 1;
    };
    print("最终i = " + str(i));
    """

    xlang = XLang()
    result = xlang.execute(code)
    print(result)


if __name__ == "__main__":
    test()
