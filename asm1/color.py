csi    = '\x1B['
red    = csi + '31;1m'
yellow = csi + '33;1m'
end    = csi + '0m'


print('Here is a %sred%s word and one in %syellow!%s' % (red, end, yellow, end))