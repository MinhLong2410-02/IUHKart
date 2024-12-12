import React, { useEffect } from 'react';
import {
    Box,
    Button,
    Checkbox,
    Flex,
    FormControl,
    FormErrorMessage,
    FormLabel,
    Heading,
    Input,
    InputGroup,
    InputRightElement,
    Link,
    Select,
    Stack,
    Step,
    StepDescription,
    StepIcon,
    StepIndicator,
    StepNumber,
    Stepper,
    StepSeparator,
    StepStatus,
    StepTitle,
    Textarea,
    useSteps
} from "@chakra-ui/react";
import { ChevronDownIcon, ViewIcon, ViewOffIcon } from "@chakra-ui/icons";
import SignUpImg from "../../assets/images/sign-ip-next-vendor.png";
import { Form, useNavigate } from 'react-router-dom';
import "./style.css";
import { getAllAddress, getAllDistrict, getAllProvince, updateAddress } from '../../api/address';


const steps = [
    {
        title: "Step 1",
        description: "Account Information"
    },
    {
        title: "Step 2",
        description: "Personal Information"
    }
]

function SignUp() {

    const navigate = useNavigate();

    const [showPassword, setShowPassword] = React.useState(false);
    const [showConfirmPassword, setShowConfirmPassword] = React.useState(false);
    const toggleShow = (currentValue, setterFunction) => {
        setterFunction(!currentValue);
    }
    const [email, setEmail] = React.useState('');
    const [shopName, setShopName] = React.useState('');
    const [phoneNumber, setPhoneNumber] = React.useState('');
    const [password, setPassword] = React.useState('');
    const [confirmPassword, setConfirmPassword] = React.useState('');
    const [emailError, setEmailError] = React.useState('');
    const [passwordError, setPasswordError] = React.useState('')
    const [confirmPasswordError, setConfirmPasswordError] = React.useState('')
    const { activeStep, setActiveStep } = useSteps({
        index: 0,
        count: steps.length,
    })

    const [province, setProvince] = React.useState([]);
    const [district, setDistrict] = React.useState([]);
    const [ward, setWard] = React.useState([]);

    const [description, setDescription] = React.useState('');
    const [IdProvince, setIdProvince] = React.useState(0);
    const [IdDistrict, setIdDistrict] = React.useState(0);
    const [IdWard, setIdWard] = React.useState(0);
    const [address, setAddress] = React.useState('');


    useEffect(() => {
        const getData = async () => {
            try {
                const response = await getAllProvince();
                console.log(response);
                setProvince(response);
            } catch (error) {
                console.log(error);
            }
        }

        getData();
    }, [])

    const handleChangeProvince = async (value) => {
        try {
            setIdProvince(Number(value));
            const data = await getAllDistrict(value);
            setDistrict(data);
        } catch (error) {
            console.error("Error fetching districts:", error);
            // Bạn có thể thêm xử lý lỗi khác nếu cần, ví dụ: hiển thị thông báo lỗi cho người dùng
        }
    }
    
    const handleChangeDistrict = async (value) => {
        try {
            setIdDistrict(Number(value));
            const data = await getAllAddress(value);
            setWard(data);
        } catch (error) {
            console.error("Error fetching wards:", error);
            // Bạn có thể thêm xử lý lỗi khác nếu cần, ví dụ: hiển thị thông báo lỗi cho người dùng
        }
    }
    
    

    const changeStep = async (e) => {
        e.preventDefault();

        const formData = new FormData();
        formData.append("province_id", Number(IdProvince));
        formData.append("district_id", Number(IdDistrict));
        formData.append("ward_id", Number(IdWard));
        formData.append("address_detail", address);
        // formData.append("description", description);
        const data = Object.fromEntries(formData.entries());
        
        const rs = await updateAddress(data);
        if (rs) {
            navigate('/home'); 
        } 
    };

    // console.log(province);

    return (
        <Flex
            width="full"
            height="full"
            flexDirection="row"
            align="flex-start"
            className="login-page justify-start"
        >
            <Box className="login-page__left flex justify-end items-end" h="100%" w="55%" >
                <img src={SignUpImg} alt="login-img" style={{ width: "100%", height: "100%" }} />
            </Box>
            <Box className="login-page__right__1 flex !flex-1 justify-start items-center" w="full" h="full">
                <Box className="login-page__right__form" mt={6} w="full">
                    <Stack spacing={15} paddingLeft={20} paddingRight={20}>
                        <Heading fontWeight={700} fontSize={50} mb={20} >Sign Up</Heading>
                        <Box className="login-page__right__form__step1">
                            <form>
                                <Stack spacing={6}>
                                    <FormControl variant="floating">
                                        <InputGroup>
                                            <Input 
                                                onChange={(e) => {
                                                    setDescription(Number(e.target.value));
                                                }}
                                                type="text"
                                            />
                                            <FormLabel fontWeight={400}>Descriptions</FormLabel>
                                            <FormErrorMessage></FormErrorMessage>
                                        </InputGroup>
                                    </FormControl>
                                    <FormControl variant="floating">
                                        <Stack flexDirection="row">
                                            <InputGroup>
                                                <Select 
                                                    onClick={(e) => {
                                                        handleChangeProvince(Number(e.target.value));
                                                    }}
                                                    icon={<ChevronDownIcon/>}
                                                >
                                                    {province?.map((item, index) => (
                                                        <option key={index} value={Number(item.province_id)}>{item.province_name}</option>
                                                    ))}
                                                </Select>
                                                <FormLabel fontWeight={400}>Province</FormLabel>
                                            </InputGroup>
                                        </Stack>
                                    </FormControl>
                                    <FormControl variant="floating">
                                        <Stack flexDirection="row">
                                            <InputGroup>
                                                <Select 
                                                    onClick={(e) => {
                                                        handleChangeDistrict(Number(e.target.value));
                                                    }}
                                                    icon={<ChevronDownIcon/>}
                                                >
                                                    {district?.map((item, index) => (
                                                        <option key={index} value={Number(item.district_id)}>{item.district_name}</option>
                                                    ))}
                                                </Select>
                                                <FormLabel fontWeight={400}>District</FormLabel>
                                            </InputGroup>
                                        </Stack>
                                    </FormControl>
                                    <FormControl variant="floating">
                                        <InputGroup>
                                            <Select 
                                            onClick={(e) => {
                                                setIdWard(Number(e.target.value));
                                            }}
                                            icon={<ChevronDownIcon/>}>
                                                {ward?.map((item, index) => (
                                                    <option key={index} value={Number(item.ward_id)}>{item.ward_name}</option>
                                                ))}
                                            </Select>
                                            <FormLabel fontWeight={400}>Ward</FormLabel>
                                        </InputGroup>
                                    </FormControl>
                                    <FormControl variant="floating">
                                        <InputGroup>
                                            <Input 
                                                type="text"
                                                onChange={(e) => {
                                                    setAddress(e.target.value);
                                                }}
                                            />
                                            <FormLabel fontWeight={400}>Address</FormLabel>
                                        </InputGroup>
                                    </FormControl>
                                    <FormControl>
                                        <button 
                                            onClick={changeStep}
                                            className='bg-[#000] w-full h-[65px] text-xl text-white py-3 rounded-[20px]'
                                        >Create Account</button>
                                        <Box textAlign="center" mt={3}>
                                            Already have an account? <Button variant="link" colorScheme="red"
                                                                            _hover={{textDecoration: "none"}}>Login</Button>
                                        </Box>
                                    </FormControl>
                                </Stack>
                            </form>
                        </Box>
                    </Stack>
                </Box>
            </Box>
        </Flex>
    );
}

export default SignUp;