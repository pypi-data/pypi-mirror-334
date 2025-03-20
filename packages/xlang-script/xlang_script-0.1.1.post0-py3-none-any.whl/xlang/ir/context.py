from .variable import Tuple, KeyValue, Lambda


class Context:
    def __init__(self):
        self.frames = []
        self.stack_pointers = []

    def new_frame(self, stack, enter_func = False, funciton_code_position = None, hidden = False):
        self.frames.append(({}, enter_func, funciton_code_position, hidden))
        self.stack_pointers.append(len(stack))

    def pop_frame(self, stack, exit_func = False):
        if exit_func:
            while len(self.frames) > 0 and not self.frames[-1][1]:
                stack_pointer = self.stack_pointers.pop()
                self.frames.pop()
                del stack[stack_pointer:]
            stack_pointer = self.stack_pointers.pop()
            self.frames.pop()
            del stack[stack_pointer:]            
        else:
            stack_pointer = self.stack_pointers.pop()
            self.frames.pop()
            del stack[stack_pointer:]
    def let(self, key, value):
        self.frames[-1][0][key] = value

    def get(self, key):
        for frame in reversed(self.frames):
            if key in frame[0]:
                return frame[0][key]
        raise KeyError(f"'{key}' not found in Context")

    def set(self, key, value):
        for frame in reversed(self.frames):
            if key in frame[0]:
                frame[0][key] = value
                return
        raise KeyError(f"'{key}' not found in Context")

    def __getitem__(self, key):
        return self.get(key)

    def __setitem__(self, key, value):
        self.set(key, value)

    def __contains__(self, key):
        for frame in reversed(self.frames):
            if key in frame[0]:
                return True
        return False

    def __str__(self):
        return f"Context({self.frames})"

    def __repr__(self):
        return str(self)

    def __del__(self):
        # if len(self.frames) > 0:
        #    raise Exception("Context not clean: frames not empty\n" + str(self.frames))
        del self.frames

    def sizeof(self):
        return len(self.frames)

    def slice_frames_and_stack(self, stack, size):
        """将堆栈和帧截断到指定大小"""
        if size < 0:
            raise ValueError("Size must be greater than 0")
        if size == 0:
            self.frames = []
            self.stack_pointers = []
            stack.clear()
        if len(self.frames) < size:
            raise ValueError("Unable to slice context: size is greater than current size")
        else:
            self.frames = self.frames[:size]
            self.stack_pointers = self.stack_pointers[:size]
            stack_pointer = self.stack_pointers[-1] if self.stack_pointers else 0
            del stack[stack_pointer:]

    def format_stack_and_frames(self, stack):
        """返回格式化的堆栈和帧信息，而非打印"""
        result = []
        collected_code_positions = []
        result.append("# Stack and Frames")

        # 格式化堆栈元素
        result.append("\n## Stack:")
        if not stack:
            result.append("  - <Empty>")
        else:
            for i, item in enumerate(stack):
                result.append(f"  - <{i}> {type(item).__name__}: `{item}`")

        # 格式化栈指针
        result.append("\n## Stack Pointers:")
        if not self.stack_pointers:
            result.append("  - <Empty>")
        else:
            for i, pointer in enumerate(self.stack_pointers):
                result.append(f"  + Frame {i} -> {pointer}")

        # 格式化变量帧
        result.append("\n## Frames")
        if not self.frames:
            result.append("  - <Empty>")
        else:
            for i, (frame, is_func, code_position, hidden) in enumerate(self.frames):
                if is_func:
                    collected_code_positions.append(code_position)
                frame_type = (
                    f"function, code_position = {code_position}" if is_func else "normal"
                )
                result.append(f"  + frame {i} ({frame_type}):")
                if hidden:
                    result.append("    - <Hidden>")
                elif not frame:
                    result.append("    - <Empty>")
                else:
                    for var_name, var_value in frame.items():
                        value_repr = str(var_value)
                        if len(value_repr) > 70:  # 截断过长的输出
                            value_repr = value_repr[:67] + "..."
                        result.append(f"    - {var_name} = `{value_repr}`")

        return "\n".join(result), collected_code_positions


    def print_stack_and_frames(self, stack):
        """保留向后兼容的打印方法"""
        error, code_positions = self.format_stack_and_frames(stack)
        print(error)
        print("\n# Executed Lambda Positions")
        for code_position in code_positions:
            print(f"  - {code_position}")
