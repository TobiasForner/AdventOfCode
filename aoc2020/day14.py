from input_utils import get_input_file_lines_no_nl
import re

p = re.compile(r'mem\[(\d*)\] = (\d*)')


def part01(lines):
    mask = {'and': 1, 'or': 0}
    memory = {}
    for line in lines:
        if line[:4] == 'mask':
            m = line[7:]
            mask['or'] = int(m .replace('X', '0'), base=2)
            mask['and'] = int(m .replace('X', '1'), base=2)
        else:
            m = p.match(line)
            address, init_value = m.groups()
            memory[address] = (int(init_value) & mask['and']) | mask['or']
    print('part01', sum(memory.values()))


def part02(lines, verbose=False):
    def get_addresses(base_address, mask):
        ret = []
        with_or_mask = int(base_address) | int(mask.replace('X', '0'), base=2)
        x_pos = []
        for i, c in enumerate(mask):
            if c == 'X':
                x_pos.append(i)
        with_or_str = f'{with_or_mask:36b}'.replace(' ', '0')
        q = [(with_or_str, x_pos)]
        while q:
            #print('queue', q)
            addr, pos = q[0]
            q = q[1:]
            if not pos:
                ret.append(addr)
                continue
            addr_0 = addr[:pos[0]] + '0' + addr[pos[0]+1:]
            addr_1 = addr[:pos[0]] + '1' + addr[pos[0]+1:]
            q.append((addr_0, pos[1:]))
            q.append((addr_1, pos[1:]))
        return ret

    mask = '1'*36
    memory = {}
    for line in lines:
        if line[:4] == 'mask':
            mask = line[7:]
        else:
            m = p.match(line)
            address, init_value = m.groups()
            addresses = get_addresses(address, mask)
            if verbose:
                print(
                    f'Writing {init_value} to addresses {addresses}')
            for a in addresses:
                memory[a] = int(init_value)
    print('part02', sum(memory.values()))


if __name__ == '__main__':
    lines = get_input_file_lines_no_nl('day14.txt')
    part01(lines)
    part02(lines)
