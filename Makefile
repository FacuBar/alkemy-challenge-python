postgres:
	docker run --name postgres12 -p 5432:5432 -e POSTGRES_USER=root -e POSTGRES_PASSWORD=password -d postgres:12-alpine

createdb:
	docker exec -it postgres12 createdb --username=root --owner=root alkemy_test

dropdb:
	docker exec -it postgres12 dropdb alkemy_test

.PHONY: postgres createdb dropdb