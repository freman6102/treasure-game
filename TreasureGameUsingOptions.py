require_relative 'Game'

# 
# Load the specified map module
#
require 'optparse'
options = {}

OptionParser.new do |opt|
  opt.on('--map_file MAP_FILE_NAME') { |o| options[:treasure_map_file] = o }
end.parse!

if options[:treasure_map_file] == nil
  options[:treasure_map_file] = "maps/TreasureMap1"
end

begin
  require_relative options[:treasure_map_file]
rescue
  puts "Unable to load treasure map file: '#{options[:treasure_map_file]}'."
  exit(1)
end

#
# Run the game
#
game = Game.new(TreasureMap::MAP)
while game.play
end

