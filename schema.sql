DROP TABLE IF EXISTS books;

CREATE TABLE books (
    id integer primary key autoincrement,
    title text not null,
    author text not null,
    created timestamp nut null default current_timestamp,
    updated timestamp nut null default current_timestamp
);

create trigger [UpdateField] after update on [books]
Begin
    update books set updated = current_timestamp where id=old.id;
end;