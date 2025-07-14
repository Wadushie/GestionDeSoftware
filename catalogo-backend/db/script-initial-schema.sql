-- CREAR LA BD catalogo
CREATE DATABASE catalogo;

-- CREAR LA TABLA public.proveedor
create table public.proveedor (
    id bigserial primary key,
    nombre text,
    direccion text,
    telefono text
);

-- CREAR LA TABLA public.categoria
create table public.categoria (
    id bigserial primary key,
    descripcion text
);

-- CREAR LA TABLA public.producto
create table public.producto (
    id bigserial primary key,
    proveedor_id bigint references proveedor(id),
    categoria_id bigint references categoria(id),
    nombre text,
    descripcion text,
    precio numeric,
    estado text
);