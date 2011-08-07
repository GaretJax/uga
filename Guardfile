

guard 'livereload' do
  watch(%r{templates/.+\.html})
  watch(%r{static/styles/.+\.css})
end

guard 'compass', :configuration_file => 'support/sass-config.rb' do
  watch(%r{support/sass/(.*)\.s[ac]ss})
end