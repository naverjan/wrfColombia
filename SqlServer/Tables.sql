USE [CCLIMATE]
GO

/****** Object:  Table [forecast].[cc_model]    Script Date: 28/12/2020 4:24:23 p. m. ******/
SET ANSI_NULLS ON
GO

SET QUOTED_IDENTIFIER ON
GO
--TABLA DE MODELO
CREATE TABLE [forecast].[cc_model](
	[id] [int] IDENTITY(1,1) NOT NULL,
	[name] [nvarchar](50) NULL,
	[description] [nvarchar](500) NULL,
	[provider] [nvarchar](50) NULL,
	[param1] [nvarchar](500) NULL,
	[param2] [nvarchar](50) NULL,
	[param3] [nvarchar](50) NULL,
	[param4] [nvarchar](50) NULL,
	[frecuencyH] [int] NULL,
 CONSTRAINT [PK_cc_model] PRIMARY KEY CLUSTERED 
(
	[id] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON) ON [DATA1]
) ON [DATA1]

GO

--Tabla de ejecuciones de procesos
SET QUOTED_IDENTIFIER ON
GO

CREATE TABLE [forecast].[cc_run](
	[id] [bigint] NOT NULL,
	[idmodel] [int] NOT NULL,
	[idstatus] [int] NULL,
 CONSTRAINT [PK_cc_run] PRIMARY KEY CLUSTERED 
(
	[id] ASC,
	[idmodel] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON) ON [DATA1]
) ON [DATA1]

GO

--TABLA DE INFORMACION
CREATE TABLE [forecast].[cc_JMStation](
	[idTime] [bigint] NOT NULL,
	[idModel] [int] NOT NULL,
	[idRun] [bigint] NOT NULL,
	[idLocation] [int] NOT NULL,
	[anio] [int] NULL,
	[mes] [int] NULL,
	[dia] [int] NULL,
	[hora] [int] NULL,
	[temperature] [float] NULL,
	[humidity] [float] NULL,
	[windSpeed] [float] NULL,
	[windDir] [float] NULL,
	[precipitation] [float] NULL,
	[solarRad] [float] NULL,
	[presure] [float] NULL,
	[ET] [float] NULL,
 CONSTRAINT [PK_cc_JMStation] PRIMARY KEY CLUSTERED 
(
	[idTime] ASC,
	[idModel] ASC,
	[idRun] ASC,
	[idLocation] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON) ON [DATA1]
) ON [DATA1]


--TABLA DE UBICACIONES

CREATE TABLE [forecast].[cc_location](
	[id] [int] IDENTITY(1,1) NOT NULL,
	[code] [nvarchar](50) NULL,
	[GMT] [int] NULL,
	[name] [nvarchar](100) NULL,
	[idEstacion] [int] NULL,
	[latitude] [float] NULL,
	[longitude] [float] NULL,
	[param1] [nvarchar](50) NULL,
 CONSTRAINT [PK_cc_location] PRIMARY KEY CLUSTERED 
(
	[id] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON) ON [DATA1]
) ON [DATA1]

GO