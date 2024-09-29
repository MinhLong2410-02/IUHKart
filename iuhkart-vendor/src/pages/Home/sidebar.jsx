import React from 'react';

import { Link, NavLink, useLocation } from 'react-router-dom';
import {
    IconButton,
    Box,
    CloseButton,
    Flex,
    Icon,
    useColorModeValue,
    Drawer,
    DrawerContent,
    Text,
    useDisclosure,
    Button,
} from '@chakra-ui/react';
// import {
//     FiHome,
//     FiTrendingUp,
//     FiCompass,
//     FiStar,
//     FiSettings,
//     FiMenu,
// } from "react-icon";

const LinkItems = [
    { path: "summary", name: 'Summary' },
    { path: "info", name: 'Info' },
    { path: "products", name: 'Products' },
    // { path: "orders", name: 'Pr' },
];

export default function SimpleSidebar({ children }) {
    const { isOpen, onOpen, onClose } = useDisclosure();
    return (
        <Box
            minH="100vh"
        // bg={useColorModeValue('gray.100', 'gray.900')}
        >
            <SidebarContent
                onClose={() => onClose()}
                display={{ base: 'none', md: 'block' }}
                className='relative'
            />
            {/* <Box
                w={{ base: 'full', md: 60 }}
                className='absolute top-[82%] bg-white h-[150px] rounded-[20px] p-4 flex justify-center items-center'>
                <Button
                    colorScheme="blue"
                    w="full"
                >
                    LogOut
                </Button>
            </Box> */}
            <Drawer
                autoFocus={false}
                isOpen={isOpen}
                placement="left"
                onClose={onClose}
                returnFocusOnClose={false}
                onOverlayClick={onClose}
                size="full">
                <DrawerContent>
                    <SidebarContent onClose={onClose} />
                </DrawerContent>
            </Drawer>
            {/* <Box ml={{ base: 0, md: 60 }} p="4">
                {children}
            </Box> */}
        </Box>
    );
}

const SidebarContent = ({ onClose, ...rest }) => {
    return (
        <Box
            bg={"white"}
            borderRight="1px"
            borderRadius={20}
            borderRightColor={useColorModeValue('gray.200', 'gray.700')}
            w={{ base: 'full', md: 60 }}
            pos="fixed"
            h="80%"
            {...rest}>
            <Flex h="20" alignItems="center" mx="8" justifyContent="space-between">
                <Text fontSize="2xl" fontFamily="monospace" fontWeight="bold">
                    Logo
                </Text>
                <CloseButton display={{ base: 'flex', md: 'none' }} onClick={onClose} />
            </Flex>
            {LinkItems.map((link) => (
                <NavItem key={link.name} path={link.path}>
                    {link.name}
                </NavItem>
            ))}
        </Box>
    );
};

const NavItem = ({ icon, children, path, ...rest }) => {
    return (
        <Link to={path} style={{ textDecoration: 'none' }} _focus={{ boxShadow: 'none' }}>
            <Flex
                align="center"
                p="4"
                mx="4"
                borderRadius="lg"
                role="group"
                cursor="pointer"
                bg={useLocation().pathname === `/${path}` ? 'cyan.400' : 'white'}
                _hover={{
                    bg: 'cyan.400',
                    color: 'white',
                }}
                {...rest}>
                {icon && (
                    <Icon
                        mr="4"
                        fontSize="16"
                        _groupHover={{
                            color: 'white',
                        }}
                        as={icon}
                    />
                )}
                {children}
            </Flex>
        </Link>
    );
};

// const MobileNav = ({ onOpen, ...rest }) => {
//     return (
//         <Flex
//             height="20"
//             alignItems="center"
//             // bg={useColorModeValue('white', 'gray.900')}
//             borderBottomWidth="1px"
//             borderBottomColor={useColorModeValue('gray.200', 'gray.700')}
//             justifyContent="flex-start"
//             {...rest}>
//             <IconButton
//                 variant="outline"
//                 onClick={onOpen}
//                 aria-label="open menu"
//             // icon={<FiMenu />}
//             />

//             <Text fontSize="2xl" ml="8" fontFamily="monospace" fontWeight="bold">
//                 Logo
//             </Text>
//         </Flex>
//     );
// };
