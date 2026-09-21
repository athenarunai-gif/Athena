-- Ablage der Morgen-Routine. Projekt zafbcpkfhtktohzjzkvj (AthenaRun).
-- Eigenes Schema, weil die Instanz geteilt ist und public die App enthaelt.

create schema if not exists buero;

create table if not exists buero.eintraege (
  id                    uuid primary key default gen_random_uuid(),
  typ                   text not null check (typ in ('kunde', 'investor')),
  name                  text not null,
  phase                 text,
  naechster_schritt     text,
  naechster_schritt_am  date,
  kontakte              text,
  worum_es_geht         text,
  meddpicc              text,
  offene_punkte         text,
  zugesagt              text,
  angelegt_am           timestamptz not null default now(),
  geaendert_am          timestamptz not null default now(),
  unique (typ, name)
);

create table if not exists buero.log (
  id          bigint generated always as identity primary key,
  eintrag_id  uuid not null references buero.eintraege(id) on delete cascade,
  am          timestamptz not null default now(),
  quelle      text,
  text        text not null
);

create index if not exists log_eintrag_am_idx on buero.log (eintrag_id, am desc);

create table if not exists buero.stand (
  id                     integer primary key default 1 check (id = 1),
  letzter_lauf           timestamptz,
  slack_verarbeitet_bis  timestamptz,
  notiz                  text
);

create table if not exists buero.gelernt (
  id    bigint generated always as identity primary key,
  am    date not null default current_date,
  text  text not null
);

create table if not exists buero.gelernt_gruende (
  id    bigint generated always as identity primary key,
  grund text not null unique
);

alter table buero.eintraege       enable row level security;
alter table buero.log             enable row level security;
alter table buero.stand           enable row level security;
alter table buero.gelernt         enable row level security;
alter table buero.gelernt_gruende enable row level security;

revoke all on schema buero from anon, authenticated;
revoke all on all tables in schema buero from anon, authenticated;
