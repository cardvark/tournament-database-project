# tournament-database-project
Udacity project.  Create and query tables with postgresql and psycopg2.

## Setup:
* Install [Vagrant](https://www.vagrantup.com/) and [Virtualbox](https://www.virtualbox.org/).
* Clone the udacity [fullstack-nanodegree-vm-repository](http://github.com/udacity/fullstack-nanodegree-vm).
* Clone or [download](https://github.com/cardvark/tournament-database-project/archive/master.zip) and extract the files from this repo into the /vagrant/tournament/ directory.
* Start the VM:  `vagrant up`
* Log into VM: `vagrant ssh`
* Navigate to /vagrant/tournament
* import DB schema, using psql:
  * `psql`
  * `\i tournament.sql`
  * `\q`
* Run the test module: `python tournament_test.py`
