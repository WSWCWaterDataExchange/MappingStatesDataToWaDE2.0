/****** Object:  StoredProcedure [Core].[LoadAggregatedAmounts]    Script Date: 12/20/2019 10:44:44 AM ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
ALTER PROCEDURE [Core].[LoadAggregatedAmounts]
(
    @RunId NVARCHAR(250),
    @AggregatedAmountTable Core.AggregatedAmountTableType READONLY
)
AS
BEGIN
    SELECT ROW_NUMBER() OVER(ORDER BY (SELECT NULL)) RowNumber, *
    INTO #TempAggregatedAmountData
    FROM @AggregatedAmountTable;
    
    --wire up the foreign keys
    SELECT
        aad.*
        ,og.OrganizationID
		,ru.ReportingUnitID
		,vb.VariableSpecificID
		,mt.MethodID
        ,wt.WaterSourceID
		,bs.Name PrimaryUseCategoryCV
		,CASE WHEN PopulationServed IS NULL AND CommunityWaterSupplySystem IS NULL 
						AND CustomerType IS NULL AND SDWISIdentifier IS NULL
						THEN 0 ELSE 1 END
					+ CASE WHEN IrrigatedAcreage IS NULL AND CropTypeCV IS NULL 
						AND IrrigationMethodCV IS NULL AND AllocationCropDutyAmount IS NULL
						THEN 0 ELSE 1 END
					+ CASE WHEN PowerGeneratedGWh IS NULL AND PowerType IS NULL
						THEN 0 ELSE 1 END CategoryCount
	INTO
		#TempJoinedAggregatedAmountData
    FROM
        #TempAggregatedAmountData aad
		LEFT OUTER JOIN Core.Organizations_dim og ON aad.OrganizationUUID = og.OrganizationUUID
		LEFT OUTER JOIN Core.ReportingUnits_dim ru ON aad.ReportingUnitUUID = ru.ReportingUnitUUID
        LEFT OUTER JOIN Core.Variables_dim vb ON aad.VariableSpecificUUID = vb.VariableSpecificUUID
        LEFT OUTER JOIN Core.Methods_dim mt ON aad.MethodUUID = mt.MethodUUID
	    LEFT OUTER JOIN CVs.BeneficialUses bs ON aad.PrimaryUseCategory = bs.Name
        LEFT OUTER JOIN Core.WaterSources_dim wt ON aad.WaterSourceUUID = wt.WaterSourceUUID;

		
    --data validation
    WITH q1 AS
    (
        SELECT 'OrganizationID Not Valid' Reason, *
        FROM #TempJoinedAggregatedAmountData
        WHERE OrganizationID IS NULL
        UNION ALL
		SELECT 'ReportingUnitID Not Valid' Reason, *
        FROM #TempJoinedAggregatedAmountData
        WHERE ReportingUnitID IS NULL
        UNION ALL
        SELECT 'VariableSpecificID Not Valid' Reason, *
        FROM #TempJoinedAggregatedAmountData
        WHERE VariableSpecificID IS NULL
		 UNION ALL
		SELECT 'MethodID Not Valid' Reason, *
        FROM #TempJoinedAggregatedAmountData
        WHERE MethodID IS NULL
        UNION ALL
        SELECT 'WaterSourceID Not Valid' Reason, *
        FROM #TempJoinedAggregatedAmountData
        WHERE WaterSourceID IS NULL
        UNION ALL
		SELECT 'Amount Not Valid' Reason, *
        FROM #TempJoinedAggregatedAmountData
        WHERE Amount IS NULL
		--//////////////////////////////s
		UNION ALL
		SELECT 'Cross Group Not Valid' Reason, *
        FROM #TempJoinedAggregatedAmountData
        WHERE CategoryCount > 1
		--//////////////////////////////////e

    )
    SELECT * INTO #TempErrorAggregatedAmountRecords FROM q1;

	
    --if we have errors, insert them and bail out
    IF EXISTS(SELECT 1 FROM #TempErrorAggregatedAmountRecords) 
    BEGIN
        INSERT INTO Core.ImportErrors ([Type], [RunId], [Data])
        VALUES ('AggregatedAmounts', @RunId, (SELECT * FROM #TempErrorAggregatedAmountRecords FOR JSON PATH));
        RETURN 1;
    END

	

    --set up missing Core.BeneficialUses_dim entries
    SELECT
        aad.RowNumber
        ,BeneficialUse = TRIM(bu.[Value])
    INTO
        #TempBeneficialUsesData
    FROM
        #TempAggregatedAmountData aad
        CROSS APPLY STRING_SPLIT(aad.BeneficialUseCategory, ',') bu
    WHERE
        aad.PrimaryUseCategory IS NOT NULL
        AND bu.[Value] IS NOT NULL
        AND LEN(TRIM(bu.[Value])) > 0;
    
    --INSERT INTO
    --    CVs.BeneficialUses(Name)
    --SELECT DISTINCT
    --    bud.BeneficialUse
    --FROM
    --    #TempBeneficialUsesData bud
    --    LEFT OUTER JOIN CVs.BeneficialUses bu ON bu.Name = bud.BeneficialUse
    --WHERE
    --    bu.Name IS NULL;

    --INSERT INTO
    --    CVs.BeneficialUses(Name)
    --SELECT DISTINCT
    --    aad.PrimaryUseCategory
    --FROM
    --    #TempAggregatedAmountData aad
    --    LEFT OUTER JOIN CVs.BeneficialUses bu ON bu.Name = aad.PrimaryUseCategory
    --WHERE
    --    bu.Name IS NULL
    --    AND aad.PrimaryUseCategory IS NOT NULL
    --    AND LEN(TRIM(aad.PrimaryUseCategory)) > 0;
    
    --set up missing Core.Date_dim entries
    WITH q1 AS
    (
        SELECT
            [Date]
        FROM
            #TempAggregatedAmountData aad
            UNPIVOT ([Date] FOR Dates IN (aad.TimeframeStart, aad.TimeframeEnd, aad.DataPublicationDate)) AS up
	)
    INSERT INTO Core.Date_dim (Date, Year)
    SELECT
        q1.[Date]
        ,YEAR(q1.[Date])
    FROM
        q1
        LEFT OUTER JOIN Core.Date_dim d ON q1.[Date] = d.[Date]
    WHERE
        d.DateID IS NULL AND q1.Date IS NOT NULL
    GROUP BY
        q1.[Date];

    --merge into Core.AggregatedAmounts_fact
    CREATE TABLE #AggregatedAmountRecords(AggregatedAmountID BIGINT, RowNumber BIGINT);
    
    WITH q1 AS
    (
        SELECT
            jaad.OrganizationID
			,jaad.ReportingUnitID
            ,jaad.VariableSpecificID
            ,jaad.PrimaryUseCategory
            ,jaad.WaterSourceID
            ,jaad.MethodID
            ,TimeframeStartID = ds.DateID
            ,TimeframeEndID = de.DateID
            ,DataPublicationDate = dp.DateID
			,jaad.DataPublicationDOI
            ,jaad.ReportYearCV
            ,jaad.Amount
            ,jaad.PopulationServed
            ,jaad.PowerGeneratedGWh
            ,jaad.IrrigatedAcreage
            ,jaad.InterbasinTransferToID
            ,jaad.InterbasinTransferFromID
			,jaad.RowNumber
			,jaad.AllocationCropDutyAmount
			,jaad.CropTypeCV
			,jaad.CustomerType
			,jaad.IrrigationMethodCV
			,jaad.CommunityWaterSupplySystem
			,jaad.SDWISIdentifier
			,jaad.PowerType			
        FROM
            #TempJoinedAggregatedAmountData jaad
           -- LEFT OUTER JOIN CVs.BeneficialUses bu ON jaad.PrimaryUseCategory = bu.Name
            LEFT OUTER JOIN Core.Date_dim ds ON jaad.TimeframeStart = ds.[Date]
            LEFT OUTER JOIN Core.Date_dim de ON jaad.TimeframeEnd = de.[Date]
            LEFT OUTER JOIN Core.Date_dim dp ON jaad.DataPublicationDate = dp.[Date]
    )
    MERGE INTO Core.AggregatedAmounts_fact AS Target
	USING q1 AS Source ON
		ISNULL(Target.OrganizationID, '') = ISNULL(Source.OrganizationID, '')
		AND ISNULL(Target.WaterSourceID, '') = ISNULL(Source.WaterSourceID, '')
		AND ISNULL(Target.VariableSpecificID, '') = ISNULL(Source.VariableSpecificID, '')
		AND ISNULL(Target.TimeframeStartID, '') = ISNULL(Source.TimeframeStartID, '')
		AND ISNULL(Target.TimeframeEndID, '') = ISNULL(Source.TimeframeEndID, '')
		AND ISNULL(Target.ReportYearCV, '') = ISNULL(Source.ReportYearCV, '')
		AND ISNULL(Target.PrimaryUseCategoryCV, '') = ISNULL(Source.PrimaryUseCategory, '')
		AND ISNULL(Target.ReportingUnitID,'') = ISNULL(Source.ReportingUnitID,'')
		AND ISNULL(Target.MethodID,'') = ISNULL(Source.MethodID,'')
		
	WHEN NOT MATCHED THEN
		INSERT
			(OrganizationID
			,ReportingUnitID
			,VariableSpecificID
			,PrimaryUseCategoryCV
			,WaterSourceID
			,MethodID
			,TimeframeStartID
			,TimeframeEndID
			,DataPublicationDateID
			,DataPublicationDOI
			,ReportYearCV
			,Amount
			,PopulationServed
			,PowerGeneratedGWh
			,IrrigatedAcreage
			,InterbasinTransferToID
			,InterbasinTransferFromID
			,AllocationCropDutyAmount
			,CropTypeCV
			,CustomerTypeCV
			,IrrigationMethodCV
			,CommunityWaterSupplySystem
			,SDWISIdentifierCV
			,PowerType
			)
		VALUES
			(Source.OrganizationID
			,Source.ReportingUnitID
			,Source.VariableSpecificID
			,Source.PrimaryUseCategory
			,Source.WaterSourceID
			,Source.MethodID
			,Source.TimeframeStartID
			,Source.TimeframeEndID
			,Source.DataPublicationDate
			,Source.DataPublicationDOI
			,Source.ReportYearCV
			,Source.Amount
			,Source.PopulationServed
			,Source.PowerGeneratedGWh
			,Source.IrrigatedAcreage
			,Source.InterbasinTransferToID
			,Source.InterbasinTransferFromID
			,Source.AllocationCropDutyAmount
			,Source.CropTypeCV
			,Source.CustomerType
			,Source.IrrigationMethodCV
			,Source.CommunityWaterSupplySystem
			,Source.SDWISIdentifier
			,Source.PowerType
			)
        WHEN MATCHED THEN
            UPDATE SET
            OrganizationID = Source.OrganizationID,
			ReportingUnitID = Source.ReportingUnitID,
			VariableSpecificID = Source.VariableSpecificID,
			PrimaryUseCategoryCV = Source.PrimaryUseCategory,
			WaterSourceID = Source.WaterSourceID,
			MethodID = Source.MethodID,
			TimeframeStartID = Source.TimeframeStartID,
			TimeframeEndID = Source.TimeframeEndID,
			DataPublicationDateID = Source.DataPublicationDate,
			DataPublicationDOI = Source.DataPublicationDOI,
			ReportYearCV = Source.ReportYearCV,
		    Amount = Source.Amount,
			PopulationServed = Source.PopulationServed,
			PowerGeneratedGWh = Source.PowerGeneratedGWh,
			IrrigatedAcreage = Source.IrrigatedAcreage,
			InterbasinTransferToID = Source.InterbasinTransferToID,
			InterbasinTransferFromID = Source.InterbasinTransferFromID,
			AllocationCropDutyAmount = Source.AllocationCropDutyAmount,
			CropTypeCV = Source.CropTypeCV,
			CustomerTypeCV = Source.CustomerType,
			IrrigationMethodCV = Source.IrrigationMethodCV,
			CommunityWaterSupplySystem = Source.CommunityWaterSupplySystem,
			SDWISIdentifierCV = Source.SDWISIdentifier,
			PowerType = Source.PowerType
		OUTPUT
			inserted.AggregatedAmountID
			,Source.RowNumber
		INTO
			#AggregatedAmountRecords;
    
	--insert into Core.AggBridge_BeneficialUses_fact
	INSERT INTO Core.AggBridge_BeneficialUses_fact (BeneficialUseCV, AggregatedAmountID)
	SELECT DISTINCT
		bu.Name
		,aar.AggregatedAmountID
	FROM
		#AggregatedAmountRecords aar
		LEFT OUTER JOIN #TempBeneficialUsesData bud ON bud.RowNumber = aar.RowNumber
		LEFT OUTER JOIN CVs.BeneficialUses bu ON bu.Name = bud.BeneficialUse
	WHERE
		bu.Name IS NOT NULL AND
        NOT EXISTS(SELECT 1 from Core.AggBridge_BeneficialUses_fact innerAB where innerAB.AggregatedAmountID = aar.AggregatedAmountID and innerAB.BeneficialUseCV = bu.Name);

	RETURN 0;
END