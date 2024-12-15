import { Box, Heading, IconButton, Radio, RadioGroup, Stack, Text } from "@chakra-ui/react";
import _ from "lodash";
import React, { useContext, useEffect, useState } from "react";

import { CloseIcon } from "@chakra-ui/icons";
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
    console.log(data);
    if (data) {
      setCategorySelected(data); // Cập nhật selected category
    }
  };

  const handleReset = () => {
    setCategorySelected(null);
   };
   console.log(categorySelected);

  return (
    <Stack marginRight="20px" spacing={4}>
      <Box display="flex" alignItems="center" justifyContent="space-between" marginBottom="15px">
        <Heading as="h3" size="lg">
          Filter
        </Heading>
        {categorySelected!=null  && (
          <IconButton
            icon={<CloseIcon />}
            onClick={handleReset}
            aria-label="Reset Filter"
            size="sm"
            variant="outline"
          />
        )}
      </Box>
      <Stack spacing={4}>
        <Box>
          <Text as="b">Categories</Text>
          <RadioGroup
            marginTop={3}
            onChange={handleChangeFilter}
            value={categorySelected ? String(categorySelected) : ""} // Đảm bảo categorySelected là chuỗi
          >
            <Stack spacing={2}>
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