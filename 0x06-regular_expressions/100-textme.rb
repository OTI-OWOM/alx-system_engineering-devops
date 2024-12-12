#!/usr/bin/env ruby

ARGV[0].each_line do |line|
  if match = line.match(/\[from:(.*?)\] \[to:(.*?)\] \[flags:(.*?)\]/)
    sender = match[1]
    receiver = match[2]
    flags = match[3]
    puts "#{sender},#{receiver},#{flags}"
  end
end
