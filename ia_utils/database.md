# BASE DE DATOS DE CLAIMVISION

```sql
-- 1. Extensiones requeridas
CREATE EXTENSION IF NOT EXISTS "postgis";
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- 2. Tipos de datos ENUM del dominio
CREATE TYPE "rol_usuario" AS ENUM (
  'Administrador_Global',
  'Operador_Aseguradora',
  'Ajustador',
  'Operador_Taller',
  'Cliente'
);

CREATE TYPE "estatus_siniestro" AS ENUM (
  'Reportado_Preliminar',
  'Asignado_A_Ajustador',
  'Peritaje_Validado',
  'Asignado_A_Taller',
  'Trabajo_Concluido',
  'Listo_Para_Entrega',
  'Entregado'
);

CREATE TYPE "severidad_dano" AS ENUM (
  'Bajo',
  'Medio',
  'Alto'
);

CREATE TYPE "estatus_comercial_aseguradora" AS ENUM (
  'Activo',
  'Suspendido',
  'Cancelado'
);

CREATE TYPE "tipo_dano" AS ENUM (
  'Abolladura',
  'Rayadura',
  'Fractura',
  'Rotura_Cristal',
  'Deformacion'
);

CREATE TYPE "estatus_cotizacion" AS ENUM (
  'Pendiente_Aprobacion',
  'Aprobada',
  'Rechazada'
);

CREATE TYPE "estatus_usuario" AS ENUM (
  'Activo',
  'Inactivo',
  'Bloqueado_Temporal',
  'Bloqueado_ARCO'
);

-- 3. Definición de Tablas con Defaults Optimizados
CREATE TABLE "aseguradoras" (
  "id" uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  "nombre" text NOT NULL,
  "rfc" text UNIQUE NOT NULL,
  "dominio_correo" text UNIQUE NOT NULL,
  "plan_suscripcion" text NOT NULL,
  "limite_peritajes_mes" integer NOT NULL,
  "peritajes_consumidos_mes" integer NOT NULL DEFAULT 0,
  "estatus_comercial" estatus_comercial_aseguradora NOT NULL DEFAULT 'Activo',
  "contacto_legal_email" text NOT NULL,
  "version" integer NOT NULL DEFAULT 1,
  "created_at" timestamp with time zone NOT NULL DEFAULT clock_timestamp(),
  "updated_at" timestamp with time zone NOT NULL DEFAULT clock_timestamp(),
  "deleted_at" timestamp with time zone
);

CREATE TABLE "usuarios" (
  "id" uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  "aseguradora_id" uuid,
  "rol" rol_usuario NOT NULL,
  "email" text UNIQUE NOT NULL,
  "password_hash" text NOT NULL,
  "nombre_completo_cifrado" text NOT NULL,
  "telefono_cifrado" text,
  "huella_vinculada" boolean NOT NULL DEFAULT false,
  "estatus_arco" estatus_usuario NOT NULL DEFAULT 'Activo',
  "version" integer NOT NULL DEFAULT 1,
  "created_at" timestamp with time zone NOT NULL DEFAULT clock_timestamp(),
  "updated_at" timestamp with time zone NOT NULL DEFAULT clock_timestamp(),
  "deleted_at" timestamp with time zone
);

CREATE TABLE "perfiles_clientes" (
  "id" uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  "usuario_id" uuid UNIQUE NOT NULL,
  "numero_poliza" text NOT NULL,
  "vigencia_poliza" date NOT NULL,
  "curp_rfc_cifrado" text NOT NULL,
  "consentimiento_aviso_privacidad" boolean NOT NULL DEFAULT false,
  "consentimiento_biometria" boolean NOT NULL DEFAULT false,
  "autoriza_transferencia_talleres" boolean NOT NULL DEFAULT false,
  "fecha_consentimiento" timestamp with time zone,
  "version" integer NOT NULL DEFAULT 1,
  "created_at" timestamp with time zone NOT NULL DEFAULT clock_timestamp(),
  "updated_at" timestamp with time zone NOT NULL DEFAULT clock_timestamp(),
  "deleted_at" timestamp with time zone
);

CREATE TABLE "ajustadores" (
  "id" uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  "usuario_id" uuid UNIQUE NOT NULL,
  "cedula_profesional" text UNIQUE NOT NULL,
  "geolocalizacion_actual" geography(Point, 4326),
  "activo_para_servicio" boolean NOT NULL DEFAULT true,
  "version" integer NOT NULL DEFAULT 1,
  "created_at" timestamp with time zone NOT NULL DEFAULT clock_timestamp(),
  "updated_at" timestamp with time zone NOT NULL DEFAULT clock_timestamp(),
  "deleted_at" timestamp with time zone
);

CREATE TABLE "talleres" (
  "id" uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  "nombre_comercial" text NOT NULL,
  "rfc" text UNIQUE NOT NULL,
  "direccion_tecnica" text NOT NULL,
  "telefono_contacto" text NOT NULL,
  "version" integer NOT NULL DEFAULT 1,
  "created_at" timestamp with time zone NOT NULL DEFAULT clock_timestamp(),
  "updated_at" timestamp with time zone NOT NULL DEFAULT clock_timestamp(),
  "deleted_at" timestamp with time zone
);

CREATE TABLE "convenio_aseguradora_taller" (
  "aseguradora_id" uuid NOT NULL,
  "taller_id" uuid NOT NULL,
  "fecha_convenio" date NOT NULL,
  "version" integer NOT NULL DEFAULT 1,
  "created_at" timestamp with time zone NOT NULL DEFAULT clock_timestamp(),
  "updated_at" timestamp with time zone NOT NULL DEFAULT clock_timestamp(),
  "deleted_at" timestamp with time zone,
  PRIMARY KEY ("aseguradora_id", "taller_id")
);

CREATE TABLE "perfiles_taller_usuarios" (
  "id" uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  "usuario_id" uuid UNIQUE NOT NULL,
  "taller_id" uuid NOT NULL,
  "puesto" text,
  "version" integer NOT NULL DEFAULT 1,
  "created_at" timestamp with time zone NOT NULL DEFAULT clock_timestamp(),
  "updated_at" timestamp with time zone NOT NULL DEFAULT clock_timestamp(),
  "deleted_at" timestamp with time zone
);

CREATE TABLE "siniestros" (
  "id" uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  "aseguradora_id" uuid NOT NULL,
  "cliente_id" uuid NOT NULL,
  "ajustador_id" uuid,
  "taller_id" uuid,
  "estatus" estatus_siniestro NOT NULL DEFAULT 'Reportado_Preliminar',
  "vehiculo_marca" text NOT NULL,
  "vehiculo_modelo" text NOT NULL,
  "vehiculo_anio" integer NOT NULL,
  "vehiculo_placas" text NOT NULL,
  "vehiculo_vin" text,
  "latitud_siniestro" numeric(10,8) NOT NULL,
  "longitud_siniestro" numeric(11,8) NOT NULL,
  "narracion_texto" text,
  "narracion_audio_url" text,
  "indicaciones_dano_interno" boolean NOT NULL DEFAULT false,
  "fecha_siniestro" timestamp with time zone NOT NULL,
  "version" integer NOT NULL DEFAULT 1,
  "created_at" timestamp with time zone NOT NULL DEFAULT clock_timestamp(),
  "updated_at" timestamp with time zone NOT NULL DEFAULT clock_timestamp(),
  "deleted_at" timestamp with time zone
);

CREATE TABLE "imagenes_siniestro" (
  "id" uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  "siniestro_id" uuid NOT NULL,
  "imagen_url" text NOT NULL,
  "es_calidad_valida" boolean NOT NULL DEFAULT true,
  "metadatos_json" jsonb,
  "version" integer NOT NULL DEFAULT 1,
  "created_at" timestamp with time zone NOT NULL DEFAULT clock_timestamp(),
  "updated_at" timestamp with time zone NOT NULL DEFAULT clock_timestamp(),
  "deleted_at" timestamp with time zone
);

CREATE TABLE "peritajes_ia" (
  "id" uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  "siniestro_id" uuid UNIQUE NOT NULL,
  "costo_estimado_ia_min" numeric(12,2) NOT NULL,
  "costo_estimado_ia_max" numeric(12,2) NOT NULL,
  "version" integer NOT NULL DEFAULT 1,
  "created_at" timestamp with time zone NOT NULL DEFAULT clock_timestamp(),
  "updated_at" timestamp with time zone NOT NULL DEFAULT clock_timestamp(),
  "deleted_at" timestamp with time zone
);

CREATE TABLE "danos_detectados_ia" (
  "id" uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  "peritaje_ia_id" uuid NOT NULL,
  "zona_vehiculo" text NOT NULL,
  "tipo" tipo_dano NOT NULL,
  "severidad" severidad_dano NOT NULL,
  "costo_estimado_reparacion" numeric(10,2) NOT NULL,
  "version" integer NOT NULL DEFAULT 1,
  "created_at" timestamp with time zone NOT NULL DEFAULT clock_timestamp(),
  "updated_at" timestamp with time zone NOT NULL DEFAULT clock_timestamp(),
  "deleted_at" timestamp with time zone
);

CREATE TABLE "peritajes_ajustador" (
  "id" uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  "siniestro_id" uuid UNIQUE NOT NULL,
  "ajustador_id" uuid NOT NULL,
  "costo_definitivo_ajustador" numeric(12,2) NOT NULL,
  "firma_digital_ajustador" text NOT NULL,
  "observaciones_campo" text,
  "version" integer NOT NULL DEFAULT 1,
  "created_at" timestamp with time zone NOT NULL DEFAULT clock_timestamp(),
  "updated_at" timestamp with time zone NOT NULL DEFAULT clock_timestamp(),
  "deleted_at" timestamp with time zone
);

CREATE TABLE "danos_ajustados_manual" (
  "id" uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  "peritaje_ajustador_id" uuid NOT NULL,
  "zona_vehiculo" text NOT NULL,
  "tipo" tipo_dano NOT NULL,
  "severidad" severidad_dano NOT NULL,
  "costo_real_reparacion" numeric(10,2) NOT NULL,
  "origen_cambio" text NOT NULL DEFAULT 'AJUSTADOR',
  "version" integer NOT NULL DEFAULT 1,
  "created_at" timestamp with time zone NOT NULL DEFAULT clock_timestamp(),
  "updated_at" timestamp with time zone NOT NULL DEFAULT clock_timestamp(),
  "deleted_at" timestamp with time zone
);

CREATE TABLE "cotizaciones_taller" (
  "id" uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  "siniestro_id" uuid NOT NULL,
  "taller_id" uuid NOT NULL,
  "monto_mano_obra" numeric(12,2) NOT NULL,
  "monto_refacciones" numeric(12,2) NOT NULL,
  "monto_total" numeric(12,2) NOT NULL,
  "desglose_pdf_url" text NOT NULL,
  "estatus" estatus_cotizacion NOT NULL DEFAULT 'Pendiente_Aprobacion',
  "observaciones_tecnicas" text,
  "version" integer NOT NULL DEFAULT 1,
  "created_at" timestamp with time zone NOT NULL DEFAULT clock_timestamp(),
  "updated_at" timestamp with time zone NOT NULL DEFAULT clock_timestamp(),
  "deleted_at" timestamp with time zone
);

CREATE TABLE "logs_auditoria" (
  "id" uuid NOT NULL DEFAULT gen_random_uuid(),
  "created_at" timestamp with time zone NOT NULL DEFAULT clock_timestamp(),
  "usuario_id" uuid,
  "aseguradora_id" uuid,
  "evento_modulo" text NOT NULL,
  "accion_realizada" text NOT NULL,
  "direccion_ip" text NOT NULL,
  "user_agent" text NOT NULL,
  "metadata_context" jsonb,
  PRIMARY KEY ("id", "created_at")
);

COMMENT ON TABLE "logs_auditoria" IS 'PARTITION BY RANGE (created_at)';

-- 4. Restricciones de Integridad Corregidas (Llaves Foráneas)
ALTER TABLE "usuarios" ADD FOREIGN KEY ("aseguradora_id") REFERENCES "aseguradoras" ("id") ON DELETE RESTRICT DEFERRABLE INITIALLY IMMEDIATE;
ALTER TABLE "perfiles_clientes" ADD FOREIGN KEY ("usuario_id") REFERENCES "usuarios" ("id") ON DELETE RESTRICT DEFERRABLE INITIALLY IMMEDIATE;
ALTER TABLE "ajustadores" ADD FOREIGN KEY ("usuario_id") REFERENCES "usuarios" ("id") ON DELETE RESTRICT DEFERRABLE INITIALLY IMMEDIATE;
ALTER TABLE "perfiles_taller_usuarios" ADD FOREIGN KEY ("usuario_id") REFERENCES "usuarios" ("id") ON DELETE RESTRICT DEFERRABLE INITIALLY IMMEDIATE;

ALTER TABLE "perfiles_taller_usuarios" ADD FOREIGN KEY ("taller_id") REFERENCES "talleres" ("id") ON DELETE RESTRICT DEFERRABLE INITIALLY IMMEDIATE;
ALTER TABLE "convenio_aseguradora_taller" ADD FOREIGN KEY ("aseguradora_id") REFERENCES "aseguradoras" ("id") ON DELETE RESTRICT DEFERRABLE INITIALLY IMMEDIATE;
ALTER TABLE "convenio_aseguradora_taller" ADD FOREIGN KEY ("taller_id") REFERENCES "talleres" ("id") ON DELETE RESTRICT DEFERRABLE INITIALLY IMMEDIATE;

ALTER TABLE "siniestros" ADD FOREIGN KEY ("aseguradora_id") REFERENCES "aseguradoras" ("id") ON DELETE RESTRICT DEFERRABLE INITIALLY IMMEDIATE;
ALTER TABLE "siniestros" ADD FOREIGN KEY ("cliente_id") REFERENCES "perfiles_clientes" ("id") ON DELETE RESTRICT DEFERRABLE INITIALLY IMMEDIATE;
ALTER TABLE "siniestros" ADD FOREIGN KEY ("ajustador_id") REFERENCES "ajustadores" ("id") ON DELETE RESTRICT DEFERRABLE INITIALLY IMMEDIATE;
ALTER TABLE "siniestros" ADD FOREIGN KEY ("taller_id") REFERENCES "talleres" ("id") ON DELETE RESTRICT DEFERRABLE INITIALLY IMMEDIATE;

ALTER TABLE "imagenes_siniestro" ADD FOREIGN KEY ("siniestro_id") REFERENCES "siniestros" ("id") ON DELETE RESTRICT DEFERRABLE INITIALLY IMMEDIATE;

ALTER TABLE "peritajes_ia" ADD FOREIGN KEY ("siniestro_id") REFERENCES "siniestros" ("id") ON DELETE RESTRICT DEFERRABLE INITIALLY IMMEDIATE;
ALTER TABLE "danos_detectados_ia" ADD FOREIGN KEY ("peritaje_ia_id") REFERENCES "peritajes_ia" ("id") ON DELETE RESTRICT DEFERRABLE INITIALLY IMMEDIATE;

ALTER TABLE "peritajes_ajustador" ADD FOREIGN KEY ("siniestro_id") REFERENCES "siniestros" ("id") ON DELETE RESTRICT DEFERRABLE INITIALLY IMMEDIATE;
ALTER TABLE "peritajes_ajustador" ADD FOREIGN KEY ("ajustador_id") REFERENCES "ajustadores" ("id") ON DELETE RESTRICT DEFERRABLE INITIALLY IMMEDIATE;
ALTER TABLE "danos_ajustados_manual" ADD FOREIGN KEY ("peritaje_ajustador_id") REFERENCES "peritajes_ajustador" ("id") ON DELETE RESTRICT DEFERRABLE INITIALLY IMMEDIATE;

ALTER TABLE "cotizaciones_taller" ADD FOREIGN KEY ("siniestro_id") REFERENCES "siniestros" ("id") ON DELETE RESTRICT DEFERRABLE INITIALLY IMMEDIATE;
ALTER TABLE "cotizaciones_taller" ADD FOREIGN KEY ("taller_id") REFERENCES "talleres" ("id") ON DELETE RESTRICT DEFERRABLE INITIALLY IMMEDIATE;

ALTER TABLE "logs_auditoria" ADD FOREIGN KEY ("usuario_id") REFERENCES "usuarios" ("id") ON DELETE SET NULL DEFERRABLE INITIALLY IMMEDIATE;
ALTER TABLE "logs_auditoria" ADD FOREIGN KEY ("aseguradora_id") REFERENCES "aseguradoras" ("id") ON DELETE SET NULL DEFERRABLE INITIALLY IMMEDIATE;
```
