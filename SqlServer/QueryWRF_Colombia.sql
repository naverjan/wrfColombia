use DBTEST;

/*** INFORMACION DE COORDENADAS ***/
--CREATE TABLE [forecast].[cc_location](
/*CREATE TABLE [cc_locationCol](
	[id] [int] NOT NULL,
	[code] [nvarchar](50) NULL,			
	[longitude] [float] NULL,
	[latitude] [float] NULL,
	[isActive] [bit] NULL DEFAULT 1
	PRIMARY KEY (id)
	)*/

SELECT count(*) as Coordinates from cc_locationCol

/*** INFORMACIÓN DE CADA PUNTO ***/
/*CREATE TABLE [cc_JMWrfColombia](
	[idTime] [bigint] NOT NULL,
	[idModel] [int] NOT NULL,
	[idRun] [bigint] NOT NULL,
	[idLocation] [int] NOT NULL,
	[year] [int] NULL,
	[month] [int] NULL,
	[day] [int] NULL,
	[hour] [int] NULL,
	[rain] [float] NULL,
	[specificHumidity] [float] NULL,
	[temperature] [float] NULL,
	[zonalWind] [float] NULL,
	[southernWind] [float] NULL,
	[incidentRadiation] [float] NULL,
	[pressureSurface] [float] NULL,
	[seaSurfaceTemp] [float] NULL,
	[cloudFraction] [float] NULL
	)*/	

use DBTEST;

select * from cc_JMWrfColombia
truncate table cc_JMWrfcolombia



CREATE TABLE [cc_model](
	[id] [int] NOT NULL,
	[name] [nvarchar](50) NULL,
	[description] [nvarchar](500) NULL,
	[provider] [nvarchar](50) NULL,
	[param1] [nvarchar](500) NULL,
	[param2] [nvarchar](50) NULL,
	[param3] [nvarchar](50) NULL,
	[param4] [nvarchar](50) NULL,
	[frecuencyH] [int] NULL
	)

CREATE TABLE [cc_run](
	[id] [bigint] NOT NULL,
	[idmodel] [int] NOT NULL,
	[idstatus] [int] NULL
	)