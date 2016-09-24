INSERT INTO Users (user_id, oauth_token, enabled)
VALUES ('mtohmaz@ncsu.edu', token, 0),
VALUES ('dtvu@ncsu.edu' , token, 0),
VALUES ('krferrit@ncsu.edu', token, 0),
VALUES ('vtduong@ncsu.edu', token, 0)

INSERT INTO Events (host_id, description, title)
VALUES ('dtvu@ncsu.edu', 'Come play basketball', 'Pick up basketball'),
VALUES ('krferrit@ncsu.edu', 'Group to work on homework together', 'Java 2 Study group'),
VALUES ('vtduong@ncsu.edu', 'Friendly lunch group for those that want to meet new people', 'Lunch at Chipotle'),
VALUES ('mtohmaz@ncsu.edu', 'Swim meetup for swimmers of any level', 'Swim meetup'),

INSERT INTO JoinedEvents (event_id, host_id)
VALUES (1, 1)
VALUES (1, 2)
VALUES (1, 3)
VALUES (1, 4)
VALUES (2, 1)
VALUES (2, 2)
VALUES (2, 3)
VALUES (2, 4)
VALUES (3, 1)

INSERT INTO Tags (display_name)
VALUES ('Sports')
VALUES ('Drinks')
VALUES ('Movies')
VALUES ('Study')
VALUES ('Food')
VALUES ('Hangout')
VALUES ('Gaming')
