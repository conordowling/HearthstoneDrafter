Vagrant.configure("2") do |config|

    config.vm.define "db" do |db|
        db.vm.hostname = "db"
        db.vm.box = "ubuntu/trusty64"
        db.vm.network :forwarded_port, guest: 27017, host: 27017
        db.vm.provision :shell, :path => "vm_provisioning/db.sh"
    end

    config.vm.define "web" do |web|
        web.vm.hostname = "web"
        web.vm.box = "ubuntu/trusty64"
        web.vm.network :forwarded_port, guest: 8080, host: 8080
        web.vm.provision :shell, :path => "vm_provisioning/web.sh"
    end
end
