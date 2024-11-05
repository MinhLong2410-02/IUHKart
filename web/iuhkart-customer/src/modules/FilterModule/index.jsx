import { useContext, useEffect, useState } from "react";
import { Box, Heading, Radio, RadioGroup, Stack, Text } from "@chakra-ui/react";
import _ from "lodash";

import productApi from "../../api/product.api";
import { ProductContext } from "../../contexts/ProductContext";

const FilterModule = () => {
  const { setCategorySelected } = useContext(ProductContext);

  const [listCategory, setListCategory] = useState([]);

  useEffect(() => {
    const getCategories = async () => {
      const data = await productApi.getProductCategory();

      setListCategory(data);
    };

    getCategories();
  }, [setListCategory]);

  const handleChangeFilter = (data) => {
    setCategorySelected(data);
  };

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
          <RadioGroup marginTop={3} onChange={handleChangeFilter}>
            <Stack>
              {!_.isEmpty(listCategory) &&
                listCategory.map((category, index) => (
                  <Radio key={index} value={category?.["category_id"]}>
                    {category?.["category_name"]}
                  </Radio>
                ))}
            </Stack>
          </RadioGroup>
        </Box>
      </Stack>
    </Stack>
  );
};

export default FilterModule;
