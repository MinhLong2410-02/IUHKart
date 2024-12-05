import React, { useContext, useEffect, useState, useMemo } from "react";
import { Box, Heading, Radio, RadioGroup, Stack, Text } from "@chakra-ui/react";
import _ from "lodash";

import productApi from "../../api/product.api";
import { ProductContext } from "../../contexts/ProductContext";

const FilterModule = React.memo(() => {
  const { setCategorySelected, selectedCategory } = useContext(ProductContext);

  const [listCategory, setListCategory] = useState([]);

  useEffect(() => {
    const getCategories = async () => {
      const data = await productApi.getProductCategory();

      setListCategory(data);
    };

    getCategories();
  }, [setListCategory]);

  const handleChangeFilter = (data) => {
    // Only update if we have a value
    if (data) {
      setCategorySelected(String(data));
    }
  };

  const memoizedCategories = useMemo(() => listCategory, [listCategory]);

  console.log('Selected Category:', selectedCategory); // Debug line

  return (
    <Stack marginRight="20px">
      <Heading as="h3" size="lg" marginBottom="15px">
        Filter
      </Heading>
      <Stack gap={5}>
        <Box>
          <Box>
            <Text as="b">Categories</Text>
          </Box>
          <RadioGroup marginTop={3} onChange={handleChangeFilter} value={String(selectedCategory)}>
            <Stack>
              {!_.isEmpty(memoizedCategories) &&
                memoizedCategories.map((category, index) => (
                  <Radio key={index} value={String(category?.["category_id"])}>
                    {category?.["category_name"]}
                  </Radio>
                ))}
            </Stack>
          </RadioGroup>
        </Box>
      </Stack>
    </Stack>
  );
});

export default FilterModule;
