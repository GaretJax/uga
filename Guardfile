

guard 'livereload' do
  watch(%r{frontend/templates/.+\.html})
  watch(%r{frontend/static/styles/.+\.css})
end

guard 'compass', :configuration_file => 'support/sass-config.rb' do
  watch(%r{support/sass/(.*)\.s[ac]ss})
end