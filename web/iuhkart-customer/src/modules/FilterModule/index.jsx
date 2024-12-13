import React, { useContext, useEffect, useState } from "react";
import { Box, Heading, Radio, RadioGroup, Stack, Text } from "@chakra-ui/react";
import _ from "lodash";

import productApi from "../../api/product.api";
import { ProductContext } from "../../contexts/ProductContext";

const FilterModule = React.memo(() => {
  const { setCategorySelected, categorySelected } = useContext(ProductContext); // Lấy categorySelected từ context

  const [listCategory, setListCategory] = useState([]);

  useEffect(() => {
    const getCategories = async () => {
      const data = await productApi.getProductCategory();
      setListCategory(data); // Cập nhật danh sách category
    };

    getCategories();
  }, []);

  const handleChangeFilter = (data) => {
    // Chỉ cập nhật khi có giá trị hợp lệ
    if (data) {
      setCategorySelected(data); // Cập nhật selected category
    }
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
          <RadioGroup
            marginTop={3}
            onChange={handleChangeFilter}
            value={categorySelected ? String(categorySelected) : ""} // Đảm bảo categorySelected là chuỗi
          >
            <Stack>
              {!_.isEmpty(listCategory) &&
                listCategory.map((category) => (
                  <Radio key={category.category_id} value={String(category.category_id)}>
                    {category.category_name}
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