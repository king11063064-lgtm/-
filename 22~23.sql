Table "PetOwner {
	"ownerID" INT [pk, increment]
    "name" VARCHAR(100) [not null]
    "contact" VARCHAR(255)
}

Table "Pets" {
	"petID" INT [pk, increment]
    "ownerID" INT [not null]
    "name" VARCHAR(100) [not null]
    "species" VARCHAR(50)
    "breed" VARCHAR(50)
}

Table "Rooms" {
	"roomID" INT [pk, increment]
    "roomNumber" VARCHAR(50) [unique, not null]
    "roomType" VARCHAR(50)
    "princePerNight" DECIMAL(10,2) [not null]
}

Table "Reservation" {
	"reservationID" INT [pk increment]
    "petID" INT [not null]
    "roomID" INT [not null]
    "startDate" DATE [not null]
    "endDate" DATE [not null]
}

Table "Services" {
	"serviceID" INT [pk, increment]
    "reservationID" INT [not null]
    "serviceName" VARCHAR(100)
    "servicePrice" DECIMAL(10,2)
}