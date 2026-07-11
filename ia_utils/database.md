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
  'Cliente',
  'Tester_Global'
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

-- 3. Definicion de Tablas con Defaults Optimizados
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

CREATE TABLE "vehiculos" (
  "id" uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  "aseguradora_id" uuid NOT NULL,
  "cliente_id" uuid NOT NULL,
  "marca" text NOT NULL,
  "modelo" text NOT NULL,
  "anio" integer NOT NULL,
  "placas" text NOT NULL,
  "vin" text,
  "color" text,
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
  "vehiculo_id" uuid,
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

-- IA Microservice tables

CREATE TABLE "inferences" (
  "id" character varying PRIMARY KEY,
  "filename" character varying NOT NULL,
  "cluster_id" integer,
  "tipo_dano" character varying,
  "severidad" character varying,
  "confianza" double precision,
  "distancia_centroide" double precision,
  "created_at" timestamp with time zone NOT NULL DEFAULT clock_timestamp()
);

CREATE TABLE "nlp_transcripciones" (
  "id" character varying PRIMARY KEY,
  "filename" character varying NOT NULL,
  "texto" text,
  "duracion_seg" double precision,
  "created_at" timestamp with time zone NOT NULL DEFAULT clock_timestamp()
);

CREATE TABLE "nlp_damage_entities" (
  "id" character varying PRIMARY KEY,
  "transcripcion_id" character varying NOT NULL,
  "tipo_dano" character varying,
  "severidad" character varying,
  "parte_afectada" character varying,
  "sintoma" character varying,
  "confianza" double precision,
  "created_at" timestamp with time zone NOT NULL DEFAULT clock_timestamp()
);

CREATE TABLE "nlp_jobs" (
  "id" character varying PRIMARY KEY,
  "filename" character varying NOT NULL,
  "status" character varying NOT NULL,
  "progress" integer DEFAULT 0,
  "result_id" character varying,
  "error" text,
  "created_at" timestamp with time zone NOT NULL DEFAULT clock_timestamp(),
  "updated_at" timestamp with time zone NOT NULL DEFAULT clock_timestamp()
);

CREATE TABLE "ocr_documents" (
  "id" character varying PRIMARY KEY,
  "filename" character varying NOT NULL,
  "text" text,
  "page_count" integer,
  "created_at" timestamp with time zone NOT NULL DEFAULT clock_timestamp()
);

CREATE TABLE "v2_predictions" (
  "id" character varying PRIMARY KEY,
  "filename" character varying NOT NULL,
  "class_id" integer,
  "tipo_dano" character varying,
  "severidad" character varying,
  "confianza" double precision,
  "prob_dist" json,
  "created_at" timestamp with time zone NOT NULL DEFAULT clock_timestamp()
);

CREATE TABLE "v2_retrain_jobs" (
  "id" character varying PRIMARY KEY,
  "status" character varying NOT NULL,
  "total_epochs" integer,
  "current_epoch" integer,
  "best_accuracy" double precision,
  "loss_history" json,
  "error" text,
  "created_at" timestamp with time zone NOT NULL DEFAULT clock_timestamp(),
  "completed_at" timestamp with time zone
);

-- 4. Restricciones de Integridad (Llaves Foraneas)
ALTER TABLE "usuarios" ADD FOREIGN KEY ("aseguradora_id") REFERENCES "aseguradoras" ("id") ON DELETE RESTRICT DEFERRABLE INITIALLY IMMEDIATE;
ALTER TABLE "perfiles_clientes" ADD FOREIGN KEY ("usuario_id") REFERENCES "usuarios" ("id") ON DELETE RESTRICT DEFERRABLE INITIALLY IMMEDIATE;
ALTER TABLE "ajustadores" ADD FOREIGN KEY ("usuario_id") REFERENCES "usuarios" ("id") ON DELETE RESTRICT DEFERRABLE INITIALLY IMMEDIATE;
ALTER TABLE "perfiles_taller_usuarios" ADD FOREIGN KEY ("usuario_id") REFERENCES "usuarios" ("id") ON DELETE RESTRICT DEFERRABLE INITIALLY IMMEDIATE;

ALTER TABLE "perfiles_taller_usuarios" ADD FOREIGN KEY ("taller_id") REFERENCES "talleres" ("id") ON DELETE RESTRICT DEFERRABLE INITIALLY IMMEDIATE;
ALTER TABLE "convenio_aseguradora_taller" ADD FOREIGN KEY ("aseguradora_id") REFERENCES "aseguradoras" ("id") ON DELETE RESTRICT DEFERRABLE INITIALLY IMMEDIATE;
ALTER TABLE "convenio_aseguradora_taller" ADD FOREIGN KEY ("taller_id") REFERENCES "talleres" ("id") ON DELETE RESTRICT DEFERRABLE INITIALLY IMMEDIATE;

ALTER TABLE "vehiculos" ADD FOREIGN KEY ("aseguradora_id") REFERENCES "aseguradoras" ("id") ON DELETE RESTRICT DEFERRABLE INITIALLY IMMEDIATE;
ALTER TABLE "vehiculos" ADD FOREIGN KEY ("cliente_id") REFERENCES "perfiles_clientes" ("id") ON DELETE RESTRICT DEFERRABLE INITIALLY IMMEDIATE;

ALTER TABLE "siniestros" ADD FOREIGN KEY ("aseguradora_id") REFERENCES "aseguradoras" ("id") ON DELETE RESTRICT DEFERRABLE INITIALLY IMMEDIATE;
ALTER TABLE "siniestros" ADD FOREIGN KEY ("cliente_id") REFERENCES "perfiles_clientes" ("id") ON DELETE RESTRICT DEFERRABLE INITIALLY IMMEDIATE;
ALTER TABLE "siniestros" ADD FOREIGN KEY ("ajustador_id") REFERENCES "ajustadores" ("id") ON DELETE RESTRICT DEFERRABLE INITIALLY IMMEDIATE;
ALTER TABLE "siniestros" ADD FOREIGN KEY ("taller_id") REFERENCES "talleres" ("id") ON DELETE RESTRICT DEFERRABLE INITIALLY IMMEDIATE;
ALTER TABLE "siniestros" ADD FOREIGN KEY ("vehiculo_id") REFERENCES "vehiculos" ("id") ON DELETE SET NULL DEFERRABLE INITIALLY IMMEDIATE;

ALTER TABLE "imagenes_siniestro" ADD FOREIGN KEY ("siniestro_id") REFERENCES "siniestros" ("id") ON DELETE RESTRICT DEFERRABLE INITIALLY IMMEDIATE;

ALTER TABLE "peritajes_ia" ADD FOREIGN KEY ("siniestro_id") REFERENCES "siniestros" ("id") ON DELETE RESTRICT DEFERRABLE INITIALLY IMMEDIATE;
ALTER TABLE "danos_detectados_ia" ADD FOREIGN KEY ("peritaje_ia_id") REFERENCES "peritajes_ia" ("id") ON DELETE RESTRICT DEFERRABLE INITIALLY IMMEDIATE;

ALTER TABLE "peritajes_ajustador" ADD FOREIGN KEY ("siniestro_id") REFERENCES "siniestros" ("id") ON DELETE RESTRICT DEFERRABLE INITIALLY IMMEDIATE;
ALTER TABLE "peritajes_ajustador" ADD FOREIGN KEY ("ajustador_id") REFERENCES "ajustadores" ("id") ON DELETE RESTRICT DEFERRABLE INITIALLY IMMEDIATE;
ALTER TABLE "danos_ajustados_manual" ADD FOREIGN KEY ("peritaje_ajustador_id") REFERENCES "peritajes_ajustador" ("id") ON DELETE RESTRICT DEFERRABLE INITIALLY IMMEDIATE;

ALTER TABLE "cotizaciones_taller" ADD FOREIGN KEY ("siniestro_id") REFERENCES "siniestros" ("id") ON DELETE RESTRICT DEFERRABLE INITIALLY IMMEDIATE;
ALTER TABLE "cotizaciones_taller" ADD FOREIGN KEY ("taller_id") REFERENCES "talleres" ("id") ON DELETE RESTRICT DEFERRABLE INITIALLY IMMEDIATE;

ALTER TABLE "nlp_damage_entities" ADD FOREIGN KEY ("transcripcion_id") REFERENCES "nlp_transcripciones" ("id") ON DELETE RESTRICT DEFERRABLE INITIALLY IMMEDIATE;

ALTER TABLE "logs_auditoria" ADD FOREIGN KEY ("usuario_id") REFERENCES "usuarios" ("id") ON DELETE SET NULL DEFERRABLE INITIALLY IMMEDIATE;
ALTER TABLE "logs_auditoria" ADD FOREIGN KEY ("aseguradora_id") REFERENCES "aseguradoras" ("id") ON DELETE SET NULL DEFERRABLE INITIALLY IMMEDIATE;

-- 5. Indices

-- ajustadores
CREATE UNIQUE INDEX ajustadores_pkey ON public.ajustadores USING btree (id);
CREATE UNIQUE INDEX ajustadores_cedula_profesional_key ON public.ajustadores USING btree (cedula_profesional);
CREATE UNIQUE INDEX ajustadores_usuario_id_key ON public.ajustadores USING btree (usuario_id);

-- aseguradoras
CREATE UNIQUE INDEX aseguradoras_pkey ON public.aseguradoras USING btree (id);
CREATE UNIQUE INDEX aseguradoras_dominio_correo_key ON public.aseguradoras USING btree (dominio_correo);
CREATE UNIQUE INDEX aseguradoras_rfc_key ON public.aseguradoras USING btree (rfc);

-- convenio_aseguradora_taller
CREATE UNIQUE INDEX convenio_aseguradora_taller_pkey ON public.convenio_aseguradora_taller USING btree (aseguradora_id, taller_id);

-- cotizaciones_taller
CREATE UNIQUE INDEX cotizaciones_taller_pkey ON public.cotizaciones_taller USING btree (id);

-- danos_ajustados_manual
CREATE UNIQUE INDEX danos_ajustados_manual_pkey ON public.danos_ajustados_manual USING btree (id);

-- danos_detectados_ia
CREATE UNIQUE INDEX danos_detectados_ia_pkey ON public.danos_detectados_ia USING btree (id);

-- imagenes_siniestro
CREATE UNIQUE INDEX imagenes_siniestro_pkey ON public.imagenes_siniestro USING btree (id);

-- inferences
CREATE UNIQUE INDEX inferences_pkey ON public.inferences USING btree (id);
CREATE INDEX idx_inferences_created_at ON public.inferences USING btree (created_at DESC);

-- logs_auditoria
CREATE UNIQUE INDEX logs_auditoria_pkey ON public.logs_auditoria USING btree (id, created_at);

-- nlp_damage_entities
CREATE UNIQUE INDEX nlp_damage_entities_pkey ON public.nlp_damage_entities USING btree (id);
CREATE INDEX idx_nlp_damage_entities_transcripcion_id ON public.nlp_damage_entities USING btree (transcripcion_id);

-- nlp_jobs
CREATE UNIQUE INDEX nlp_jobs_pkey ON public.nlp_jobs USING btree (id);
CREATE INDEX idx_nlp_jobs_created_at ON public.nlp_jobs USING btree (created_at DESC);
CREATE INDEX idx_nlp_jobs_status ON public.nlp_jobs USING btree (status);

-- nlp_transcripciones
CREATE UNIQUE INDEX nlp_transcripciones_pkey ON public.nlp_transcripciones USING btree (id);
CREATE INDEX idx_nlp_transcripciones_created_at ON public.nlp_transcripciones USING btree (created_at DESC);

-- ocr_documents
CREATE UNIQUE INDEX ocr_documents_pkey ON public.ocr_documents USING btree (id);
CREATE INDEX idx_ocr_documents_created_at ON public.ocr_documents USING btree (created_at DESC);

-- perfiles_clientes
CREATE UNIQUE INDEX perfiles_clientes_pkey ON public.perfiles_clientes USING btree (id);
CREATE UNIQUE INDEX perfiles_clientes_usuario_id_key ON public.perfiles_clientes USING btree (usuario_id);

-- perfiles_taller_usuarios
CREATE UNIQUE INDEX perfiles_taller_usuarios_pkey ON public.perfiles_taller_usuarios USING btree (id);
CREATE UNIQUE INDEX perfiles_taller_usuarios_usuario_id_key ON public.perfiles_taller_usuarios USING btree (usuario_id);

-- peritajes_ajustador
CREATE UNIQUE INDEX peritajes_ajustador_pkey ON public.peritajes_ajustador USING btree (id);
CREATE UNIQUE INDEX peritajes_ajustador_siniestro_id_key ON public.peritajes_ajustador USING btree (siniestro_id);

-- peritajes_ia
CREATE UNIQUE INDEX peritajes_ia_pkey ON public.peritajes_ia USING btree (id);
CREATE UNIQUE INDEX peritajes_ia_siniestro_id_key ON public.peritajes_ia USING btree (siniestro_id);

-- siniestros
CREATE UNIQUE INDEX siniestros_pkey ON public.siniestros USING btree (id);
CREATE INDEX idx_siniestros_vehiculo_id ON public.siniestros USING btree (vehiculo_id);

-- talleres
CREATE UNIQUE INDEX talleres_pkey ON public.talleres USING btree (id);
CREATE UNIQUE INDEX talleres_rfc_key ON public.talleres USING btree (rfc);

-- usuarios
CREATE UNIQUE INDEX usuarios_pkey ON public.usuarios USING btree (id);
CREATE UNIQUE INDEX usuarios_email_key ON public.usuarios USING btree (email);

-- vehiculos
CREATE UNIQUE INDEX vehiculos_pkey ON public.vehiculos USING btree (id);
CREATE INDEX idx_vehiculos_aseguradora_id ON public.vehiculos USING btree (aseguradora_id);
CREATE INDEX idx_vehiculos_cliente_id ON public.vehiculos USING btree (cliente_id);

-- v2_predictions
CREATE UNIQUE INDEX v2_predictions_pkey ON public.v2_predictions USING btree (id);

-- v2_retrain_jobs
CREATE UNIQUE INDEX v2_retrain_jobs_pkey ON public.v2_retrain_jobs USING btree (id);
```
