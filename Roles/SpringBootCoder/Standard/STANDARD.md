# SpringBoot 编码规范文档

## 1. 概述

### 1.1 文档目的
本文档定义了SpringBoot项目的编码规范，旨在确保代码的一致性、可读性、可维护性和安全性，提高开发效率和代码质量。

### 1.2 适用范围
本规范适用于所有基于SpringBoot框架的企业级应用开发，包括Web应用、微服务、RESTful API等。

### 1.3 核心原则
- **约定优于配置**: 遵循SpringBoot的默认约定，减少显式配置
- **单一职责**: 每个类和方法应只负责一个功能
- **依赖注入**: 使用依赖注入管理对象生命周期
- **面向接口编程**: 优先使用接口而非实现类
- **RESTful设计**: 遵循REST架构风格设计API

## 2. 项目结构规范

### 2.1 包结构规范
```
com.company.project
├── config/              # 配置类
│   ├── SecurityConfig.java
│   ├── SwaggerConfig.java
│   └── WebMvcConfig.java
├── controller/          # 控制器层
│   └── UserController.java
├── service/             # 业务逻辑层
│   ├── UserService.java
│   └── impl/
│       └── UserServiceImpl.java
├── repository/          # 数据访问层（JPA）
│   └── UserRepository.java
├── mapper/              # 数据访问层（MyBatis）
│   └── UserMapper.java
├── entity/              # 实体类（对应数据库表）
│   └── User.java
├── dto/                 # 数据传输对象
│   ├── UserDTO.java
│   └── UserCreateDTO.java
├── vo/                  # 视图对象
│   └── UserVO.java
├── exception/           # 异常处理
│   ├── GlobalExceptionHandler.java
│   ├── BusinessException.java
│   └── ErrorCode.java
├── util/                # 工具类
│   └── DateUtil.java
├── enums/               # 枚举类
│   └── UserStatus.java
├── aspect/              # 切面类
│   └── LogAspect.java
└── Application.java     # 启动类
```

### 2.2 命名规范

#### 2.2.1 包命名
- 全部使用小写字母
- 使用有意义的名词
- 示例：`com.example.user.service`

#### 2.2.2 类命名
- **大驼峰命名法**（PascalCase）
- 类名应清晰表达其职责
- 示例：
  ```java
  // Controller层
  public class UserController {}
  
  // Service层
  public interface UserService {}
  public class UserServiceImpl implements UserService {}
  
  // Repository层
  public interface UserRepository extends JpaRepository<User, Long> {}
  
  // Entity层
  @Entity
  @Table(name = "t_user")
  public class User {}
  
  // DTO层
  public class UserDTO {}
  
  // VO层
  public class UserVO {}
  ```

#### 2.2.3 方法命名
- **小驼峰命名法**（camelCase）
- 方法名应以动词开头
- 示例：
  ```java
  // 查询方法
  public User findById(Long id) {}
  public List<User> findAll() {}
  public User getByUsername(String username) {}
  
  // 保存方法
  public User save(User user) {}
  public User create(UserCreateDTO dto) {}
  
  // 更新方法
  public User update(Long id, UserUpdateDTO dto) {}
  
  // 删除方法
  public void deleteById(Long id) {}
  
  // 业务方法
  public boolean existsByEmail(String email) {}
  public long countByStatus(UserStatus status) {}
  ```

#### 2.2.4 变量命名
- **小驼峰命名法**（camelCase）
- 变量名应具有描述性
- 示例：
  ```java
  // 正确
  private String userName;
  private Integer userAge;
  private List<User> userList;
  
  // 错误
  private String un;  // 过于简洁
  private Integer UserAge;  // 首字母大写
  ```

#### 2.2.5 常量命名
- **全大写字母**，单词间用下划线分隔
- 示例：
  ```java
  public static final String DEFAULT_PASSWORD = "123456";
  public static final Integer MAX_PAGE_SIZE = 100;
  public static final String JWT_SECRET = "your-secret-key";
  ```

## 3. 注解使用规范

### 3.1 核心注解

#### 3.1.1 Spring注解
```java
// 组件注解
@Controller        // 控制器
@RestController    // REST控制器（@Controller + @ResponseBody）
@Service           // 业务逻辑层
@Repository        // 数据访问层
@Component         // 通用组件
@Configuration     // 配置类

// 依赖注入
@Autowired         // 字段注入（不推荐）
@Resource          // JSR-250注解
@Inject            // JSR-330注解
// 推荐：构造器注入（无需注解，Spring 4.3+）

// 配置注解
@Value             // 属性注入
@ConfigurationProperties  // 配置属性绑定
@PropertySource    // 属性文件源

// 条件注解
@ConditionalOnProperty    // 属性条件
@ConditionalOnClass       // 类存在条件
@ConditionalOnMissingBean // Bean不存在条件
```

#### 3.1.2 Spring MVC注解
```java
// 请求映射
@RequestMapping           // 通用请求映射
@GetMapping              // GET请求
@PostMapping             // POST请求
@PutMapping              // PUT请求
@DeleteMapping           // DELETE请求
@PatchMapping            // PATCH请求

// 参数绑定
@RequestParam            // 查询参数
@PathVariable            // 路径变量
@RequestBody             // 请求体
@RequestHeader           // 请求头
@CookieValue             // Cookie值
@ModelAttribute          // 模型属性

// 响应处理
@ResponseBody            // 响应体
@ResponseStatus          // 响应状态码
```

#### 3.1.3 Spring Data JPA注解
```java
// 实体类
@Entity                  // 实体类
@Table                   // 表映射
@Id                      // 主键
@GeneratedValue          // 主键生成策略
@Column                  // 列映射
@OneToMany              // 一对多关系
@ManyToOne              // 多对一关系
@ManyToMany             // 多对多关系
@JoinColumn             // 外键列

// 生命周期回调
@PrePersist             // 持久化前
@PostPersist            // 持久化后
@PreUpdate              // 更新前
@PostUpdate             // 更新后
@PreRemove              // 删除前
@PostRemove             // 删除后
```

### 3.2 注解使用示例

#### 3.2.1 Controller层
```java
@RestController
@RequestMapping("/api/v1/users")
@Validated
public class UserController {
    
    private final UserService userService;
    
    // 构造器注入（推荐）
    public UserController(UserService userService) {
        this.userService = userService;
    }
    
    @GetMapping("/{id}")
    public Result<UserVO> getById(@PathVariable Long id) {
        UserVO user = userService.findById(id);
        return Result.success(user);
    }
    
    @PostMapping
    @ResponseStatus(HttpStatus.CREATED)
    public Result<UserVO> create(@Valid @RequestBody UserCreateDTO dto) {
        UserVO user = userService.create(dto);
        return Result.success(user);
    }
    
    @PutMapping("/{id}")
    public Result<UserVO> update(
            @PathVariable Long id,
            @Valid @RequestBody UserUpdateDTO dto) {
        UserVO user = userService.update(id, dto);
        return Result.success(user);
    }
    
    @DeleteMapping("/{id}")
    @ResponseStatus(HttpStatus.NO_CONTENT)
    public void delete(@PathVariable Long id) {
        userService.deleteById(id);
    }
    
    @GetMapping
    public Result<Page<UserVO>> list(
            @RequestParam(defaultValue = "0") Integer page,
            @RequestParam(defaultValue = "10") Integer size,
            @RequestParam(required = false) String keyword) {
        Page<UserVO> userPage = userService.list(page, size, keyword);
        return Result.success(userPage);
    }
}
```

#### 3.2.2 Service层
```java
public interface UserService {
    UserVO findById(Long id);
    UserVO create(UserCreateDTO dto);
    UserVO update(Long id, UserUpdateDTO dto);
    void deleteById(Long id);
    Page<UserVO> list(Integer page, Integer size, String keyword);
}

@Service
@Transactional
public class UserServiceImpl implements UserService {
    
    private final UserRepository userRepository;
    private final UserMapper userMapper;
    
    public UserServiceImpl(UserRepository userRepository, UserMapper userMapper) {
        this.userRepository = userRepository;
        this.userMapper = userMapper;
    }
    
    @Override
    @Transactional(readOnly = true)
    public UserVO findById(Long id) {
        User user = userRepository.findById(id)
                .orElseThrow(() -> new BusinessException(ErrorCode.USER_NOT_FOUND));
        return userMapper.toVO(user);
    }
    
    @Override
    public UserVO create(UserCreateDTO dto) {
        // 检查邮箱是否已存在
        if (userRepository.existsByEmail(dto.getEmail())) {
            throw new BusinessException(ErrorCode.EMAIL_ALREADY_EXISTS);
        }
        
        User user = userMapper.toEntity(dto);
        user.setPassword(encodePassword(dto.getPassword()));
        user = userRepository.save(user);
        
        return userMapper.toVO(user);
    }
    
    @Override
    public UserVO update(Long id, UserUpdateDTO dto) {
        User user = userRepository.findById(id)
                .orElseThrow(() -> new BusinessException(ErrorCode.USER_NOT_FOUND));
        
        userMapper.updateEntity(dto, user);
        user = userRepository.save(user);
        
        return userMapper.toVO(user);
    }
    
    @Override
    public void deleteById(Long id) {
        if (!userRepository.existsById(id)) {
            throw new BusinessException(ErrorCode.USER_NOT_FOUND);
        }
        userRepository.deleteById(id);
    }
    
    @Override
    @Transactional(readOnly = true)
    public Page<UserVO> list(Integer page, Integer size, String keyword) {
        Pageable pageable = PageRequest.of(page, size, Sort.by("createTime").descending());
        Page<User> userPage;
        
        if (StringUtils.hasText(keyword)) {
            userPage = userRepository.findByKeyword(keyword, pageable);
        } else {
            userPage = userRepository.findAll(pageable);
        }
        
        return userPage.map(userMapper::toVO);
    }
    
    private String encodePassword(String password) {
        return BCrypt.hashpw(password, BCrypt.gensalt());
    }
}
```

#### 3.2.3 Repository层
```java
@Repository
public interface UserRepository extends JpaRepository<User, Long>, JpaSpecificationExecutor<User> {
    
    // 方法命名查询
    Optional<User> findByEmail(String email);
    
    boolean existsByEmail(String email);
    
    List<User> findByStatus(UserStatus status);
    
    @Query("SELECT u FROM User u WHERE " +
           "LOWER(u.username) LIKE LOWER(CONCAT('%', :keyword, '%')) OR " +
           "LOWER(u.email) LIKE LOWER(CONCAT('%', :keyword, '%'))")
    Page<User> findByKeyword(@Param("keyword") String keyword, Pageable pageable);
    
    @Modifying
    @Query("UPDATE User u SET u.status = :status WHERE u.id = :id")
    int updateStatus(@Param("id") Long id, @Param("status") UserStatus status);
}
```

## 4. 实体类规范

### 4.1 基础实体类
```java
@MappedSuperclass
@EntityListeners(AuditingEntityListener.class)
public abstract class BaseEntity {
    
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;
    
    @CreatedDate
    @Column(name = "create_time", updatable = false)
    private LocalDateTime createTime;
    
    @LastModifiedDate
    @Column(name = "update_time")
    private LocalDateTime updateTime;
    
    @CreatedBy
    @Column(name = "create_by", updatable = false, length = 50)
    private String createBy;
    
    @LastModifiedBy
    @Column(name = "update_by", length = 50)
    private String updateBy;
    
    @Column(name = "deleted")
    private Boolean deleted = false;
    
    // Getters and Setters
}
```

### 4.2 具体实体类
```java
@Entity
@Table(name = "t_user")
@Cacheable
@org.hibernate.annotations.Cache(usage = CacheConcurrencyStrategy.READ_WRITE)
public class User extends BaseEntity {
    
    @Column(name = "username", nullable = false, unique = true, length = 50)
    private String username;
    
    @Column(name = "password", nullable = false, length = 100)
    private String password;
    
    @Column(name = "email", nullable = false, unique = true, length = 100)
    private String email;
    
    @Column(name = "phone", length = 20)
    private String phone;
    
    @Column(name = "avatar", length = 255)
    private String avatar;
    
    @Enumerated(EnumType.STRING)
    @Column(name = "status", nullable = false, length = 20)
    private UserStatus status = UserStatus.ACTIVE;
    
    @Column(name = "last_login_time")
    private LocalDateTime lastLoginTime;
    
    @ManyToMany(fetch = FetchType.LAZY)
    @JoinTable(
        name = "t_user_role",
        joinColumns = @JoinColumn(name = "user_id"),
        inverseJoinColumns = @JoinColumn(name = "role_id")
    )
    @org.hibernate.annotations.Cache(usage = CacheConcurrencyStrategy.READ_WRITE)
    private Set<Role> roles = new HashSet<>();
    
    // Getters and Setters
    
    @PrePersist
    public void prePersist() {
        this.createTime = LocalDateTime.now();
        this.updateTime = LocalDateTime.now();
    }
    
    @PreUpdate
    public void preUpdate() {
        this.updateTime = LocalDateTime.now();
    }
}
```

## 5. 异常处理规范

### 5.1 自定义异常
```java
public class BusinessException extends RuntimeException {
    
    private final ErrorCode errorCode;
    
    public BusinessException(ErrorCode errorCode) {
        super(errorCode.getMessage());
        this.errorCode = errorCode;
    }
    
    public BusinessException(ErrorCode errorCode, String message) {
        super(message);
        this.errorCode = errorCode;
    }
    
    public BusinessException(ErrorCode errorCode, Throwable cause) {
        super(errorCode.getMessage(), cause);
        this.errorCode = errorCode;
    }
    
    public ErrorCode getErrorCode() {
        return errorCode;
    }
}
```

### 5.2 错误码枚举
```java
public enum ErrorCode {
    
    // 通用错误
    SUCCESS(0, "成功"),
    UNKNOWN_ERROR(1, "未知错误"),
    INVALID_PARAMETER(2, "参数错误"),
    
    // 用户相关错误
    USER_NOT_FOUND(1001, "用户不存在"),
    EMAIL_ALREADY_EXISTS(1002, "邮箱已存在"),
    USERNAME_ALREADY_EXISTS(1003, "用户名已存在"),
    INVALID_PASSWORD(1004, "密码错误"),
    
    // 认证相关错误
    UNAUTHORIZED(2001, "未授权"),
    TOKEN_EXPIRED(2002, "Token已过期"),
    TOKEN_INVALID(2003, "Token无效"),
    ACCESS_DENIED(2004, "无权限访问"),
    
    // 业务相关错误
    RESOURCE_NOT_FOUND(3001, "资源不存在"),
    RESOURCE_ALREADY_EXISTS(3002, "资源已存在"),
    OPERATION_FAILED(3003, "操作失败");
    
    private final int code;
    private final String message;
    
    ErrorCode(int code, String message) {
        this.code = code;
        this.message = message;
    }
    
    public int getCode() {
        return code;
    }
    
    public String getMessage() {
        return message;
    }
}
```

### 5.3 全局异常处理器
```java
@RestControllerAdvice
@Slf4j
public class GlobalExceptionHandler {
    
    /**
     * 处理业务异常
     */
    @ExceptionHandler(BusinessException.class)
    public Result<Void> handleBusinessException(BusinessException e) {
        log.warn("业务异常: {}", e.getMessage());
        return Result.fail(e.getErrorCode());
    }
    
    /**
     * 处理参数校验异常
     */
    @ExceptionHandler(MethodArgumentNotValidException.class)
    public Result<Void> handleValidationException(MethodArgumentNotValidException e) {
        BindingResult bindingResult = e.getBindingResult();
        String message = bindingResult.getFieldErrors().stream()
                .map(FieldError::getDefaultMessage)
                .collect(Collectors.joining(", "));
        log.warn("参数校验失败: {}", message);
        return Result.fail(ErrorCode.INVALID_PARAMETER, message);
    }
    
    /**
     * 处理约束违反异常
     */
    @ExceptionHandler(ConstraintViolationException.class)
    public Result<Void> handleConstraintViolationException(ConstraintViolationException e) {
        String message = e.getConstraintViolations().stream()
                .map(ConstraintViolation::getMessage)
                .collect(Collectors.joining(", "));
        log.warn("约束违反: {}", message);
        return Result.fail(ErrorCode.INVALID_PARAMETER, message);
    }
    
    /**
     * 处理认证异常
     */
    @ExceptionHandler(AuthenticationException.class)
    @ResponseStatus(HttpStatus.UNAUTHORIZED)
    public Result<Void> handleAuthenticationException(AuthenticationException e) {
        log.warn("认证失败: {}", e.getMessage());
        return Result.fail(ErrorCode.UNAUTHORIZED);
    }
    
    /**
     * 处理访问拒绝异常
     */
    @ExceptionHandler(AccessDeniedException.class)
    @ResponseStatus(HttpStatus.FORBIDDEN)
    public Result<Void> handleAccessDeniedException(AccessDeniedException e) {
        log.warn("访问被拒绝: {}", e.getMessage());
        return Result.fail(ErrorCode.ACCESS_DENIED);
    }
    
    /**
     * 处理其他异常
     */
    @ExceptionHandler(Exception.class)
    @ResponseStatus(HttpStatus.INTERNAL_SERVER_ERROR)
    public Result<Void> handleException(Exception e) {
        log.error("系统异常", e);
        return Result.fail(ErrorCode.UNKNOWN_ERROR);
    }
}
```

## 6. 统一响应格式

### 6.1 响应结果类
```java
@Data
@NoArgsConstructor
@AllArgsConstructor
public class Result<T> {
    
    private Integer code;
    private String message;
    private T data;
    private Long timestamp;
    
    public static <T> Result<T> success(T data) {
        return new Result<>(ErrorCode.SUCCESS.getCode(), 
                           ErrorCode.SUCCESS.getMessage(), 
                           data, 
                           System.currentTimeMillis());
    }
    
    public static <T> Result<T> success() {
        return success(null);
    }
    
    public static <T> Result<T> fail(ErrorCode errorCode) {
        return new Result<>(errorCode.getCode(), 
                           errorCode.getMessage(), 
                           null, 
                           System.currentTimeMillis());
    }
    
    public static <T> Result<T> fail(ErrorCode errorCode, String message) {
        return new Result<>(errorCode.getCode(), 
                           message, 
                           null, 
                           System.currentTimeMillis());
    }
    
    public boolean isSuccess() {
        return ErrorCode.SUCCESS.getCode().equals(this.code);
    }
}
```

### 6.2 分页响应类
```java
@Data
@NoArgsConstructor
@AllArgsConstructor
public class PageResult<T> {
    
    private List<T> content;
    private Long totalElements;
    private Integer totalPages;
    private Integer pageNumber;
    private Integer pageSize;
    private Boolean first;
    private Boolean last;
    
    public static <T> PageResult<T> of(Page<T> page) {
        return new PageResult<>(
            page.getContent(),
            page.getTotalElements(),
            page.getTotalPages(),
            page.getNumber(),
            page.getSize(),
            page.isFirst(),
            page.isLast()
        );
    }
}
```

## 7. 参数校验规范

### 7.1 常用校验注解
```java
public class UserCreateDTO {
    
    @NotBlank(message = "用户名不能为空")
    @Size(min = 3, max = 50, message = "用户名长度必须在3-50个字符之间")
    @Pattern(regexp = "^[a-zA-Z0-9_]+$", message = "用户名只能包含字母、数字和下划线")
    private String username;
    
    @NotBlank(message = "密码不能为空")
    @Size(min = 6, max = 20, message = "密码长度必须在6-20个字符之间")
    private String password;
    
    @NotBlank(message = "邮箱不能为空")
    @Email(message = "邮箱格式不正确")
    private String email;
    
    @Pattern(regexp = "^1[3-9]\\d{9}$", message = "手机号格式不正确")
    private String phone;
    
    @Min(value = 0, message = "年龄不能小于0")
    @Max(value = 150, message = "年龄不能大于150")
    private Integer age;
    
    @NotNull(message = "状态不能为空")
    private UserStatus status;
}
```

### 7.2 自定义校验注解
```java
@Target({ElementType.FIELD})
@Retention(RetentionPolicy.RUNTIME)
@Constraint(validatedBy = PhoneValidator.class)
public @interface Phone {
    
    String message() default "手机号格式不正确";
    
    Class<?>[] groups() default {};
    
    Class<? extends Payload>[] payload() default {};
}

public class PhoneValidator implements ConstraintValidator<Phone, String> {
    
    private static final Pattern PATTERN = Pattern.compile("^1[3-9]\\d{9}$");
    
    @Override
    public boolean isValid(String value, ConstraintValidatorContext context) {
        if (value == null || value.isEmpty()) {
            return true;  // 允许为空，由@NotBlank控制
        }
        return PATTERN.matcher(value).matches();
    }
}
```

## 8. 配置文件规范

### 8.1 application.yml
```yaml
spring:
  application:
    name: springboot-project
  
  # 数据源配置
  datasource:
    driver-class-name: com.mysql.cj.jdbc.Driver
    url: jdbc:mysql://localhost:3306/db_name?useUnicode=true&characterEncoding=utf8&useSSL=false&serverTimezone=Asia/Shanghai
    username: root
    password: root
    hikari:
      minimum-idle: 5
      maximum-pool-size: 20
      connection-timeout: 30000
      idle-timeout: 600000
      max-lifetime: 1800000
  
  # JPA配置
  jpa:
    hibernate:
      ddl-auto: update
    show-sql: false
    properties:
      hibernate:
        format_sql: true
        dialect: org.hibernate.dialect.MySQL8Dialect
  
  # Redis配置
  redis:
    host: localhost
    port: 6379
    password:
    database: 0
    timeout: 5000
    lettuce:
      pool:
        max-active: 8
        max-idle: 8
        min-idle: 0
  
  # 缓存配置
  cache:
    type: redis
    redis:
      time-to-live: 600000
  
  # 文件上传配置
  servlet:
    multipart:
      max-file-size: 10MB
      max-request-size: 100MB
  
  # Jackson配置
  jackson:
    date-format: yyyy-MM-dd HH:mm:ss
    time-zone: GMT+8
    serialization:
      write-dates-as-timestamps: false
      fail-on-empty-beans: false
    deserialization:
      fail-on-unknown-properties: false

# 服务器配置
server:
  port: 8080
  servlet:
    context-path: /api
  tomcat:
    uri-encoding: UTF-8
    max-threads: 200
    accept-count: 100

# 日志配置
logging:
  level:
    root: INFO
    com.example.project: DEBUG
    org.springframework.web: DEBUG
    org.hibernate.SQL: DEBUG
  pattern:
    console: "%d{yyyy-MM-dd HH:mm:ss} [%thread] %-5level %logger{50} - %msg%n"
  file:
    name: logs/application.log
    max-size: 10MB
    max-history: 30

# 自定义配置
app:
  jwt:
    secret: your-secret-key
    expiration: 86400000  # 24小时
  upload:
    path: /data/upload
  cors:
    allowed-origins: http://localhost:3000
```

### 8.2 多环境配置
```yaml
# application-dev.yml
spring:
  datasource:
    url: jdbc:mysql://localhost:3306/db_dev
    username: root
    password: root

logging:
  level:
    com.example.project: DEBUG

# application-prod.yml
spring:
  datasource:
    url: jdbc:mysql://prod-db:3306/db_prod
    username: prod_user
    password: ${DB_PASSWORD}

logging:
  level:
    com.example.project: INFO
```

## 9. 安全规范

### 9.1 Spring Security配置
```java
@Configuration
@EnableWebSecurity
@EnableGlobalMethodSecurity(prePostEnabled = true)
public class SecurityConfig {
    
    @Bean
    public PasswordEncoder passwordEncoder() {
        return new BCryptPasswordEncoder();
    }
    
    @Bean
    public SecurityFilterChain filterChain(HttpSecurity http) throws Exception {
        http
            .csrf().disable()
            .sessionManagement().sessionCreationPolicy(SessionCreationPolicy.STATELESS)
            .and()
            .authorizeRequests()
                .antMatchers("/auth/**").permitAll()
                .antMatchers("/public/**").permitAll()
                .antMatchers(HttpMethod.GET, "/api/**").authenticated()
                .antMatchers(HttpMethod.POST, "/api/**").hasRole("ADMIN")
                .anyRequest().authenticated()
            .and()
            .addFilterBefore(jwtAuthenticationFilter(), UsernamePasswordAuthenticationFilter.class)
            .exceptionHandling()
                .authenticationEntryPoint(jwtAuthenticationEntryPoint)
                .accessDeniedHandler(jwtAccessDeniedHandler);
        
        return http.build();
    }
}
```

### 9.2 密码加密
```java
@Service
public class AuthServiceImpl implements AuthService {
    
    private final PasswordEncoder passwordEncoder;
    
    public boolean checkPassword(String rawPassword, String encodedPassword) {
        return passwordEncoder.matches(rawPassword, encodedPassword);
    }
    
    public String encodePassword(String rawPassword) {
        return passwordEncoder.encode(rawPassword);
    }
}
```

## 10. 测试规范

### 10.1 单元测试
```java
@ExtendWith(MockitoExtension.class)
class UserServiceTest {
    
    @Mock
    private UserRepository userRepository;
    
    @Mock
    private UserMapper userMapper;
    
    @InjectMocks
    private UserServiceImpl userService;
    
    @Test
    void findById_ShouldReturnUser_WhenUserExists() {
        // Given
        Long userId = 1L;
        User user = new User();
        user.setId(userId);
        user.setUsername("testuser");
        
        UserVO userVO = new UserVO();
        userVO.setId(userId);
        userVO.setUsername("testuser");
        
        when(userRepository.findById(userId)).thenReturn(Optional.of(user));
        when(userMapper.toVO(user)).thenReturn(userVO);
        
        // When
        UserVO result = userService.findById(userId);
        
        // Then
        assertNotNull(result);
        assertEquals(userId, result.getId());
        assertEquals("testuser", result.getUsername());
        
        verify(userRepository, times(1)).findById(userId);
        verify(userMapper, times(1)).toVO(user);
    }
    
    @Test
    void findById_ShouldThrowException_WhenUserNotFound() {
        // Given
        Long userId = 999L;
        when(userRepository.findById(userId)).thenReturn(Optional.empty());
        
        // When & Then
        assertThrows(BusinessException.class, () -> {
            userService.findById(userId);
        });
        
        verify(userRepository, times(1)).findById(userId);
        verify(userMapper, never()).toVO(any());
    }
}
```

### 10.2 集成测试
```java
@SpringBootTest
@AutoConfigureMockMvc
@Transactional
class UserControllerIntegrationTest {
    
    @Autowired
    private MockMvc mockMvc;
    
    @Autowired
    private UserRepository userRepository;
    
    @Autowired
    private PasswordEncoder passwordEncoder;
    
    @BeforeEach
    void setUp() {
        userRepository.deleteAll();
    }
    
    @Test
    void createUser_ShouldReturnCreatedUser() throws Exception {
        // Given
        UserCreateDTO dto = new UserCreateDTO();
        dto.setUsername("testuser");
        dto.setPassword("password123");
        dto.setEmail("test@example.com");
        
        // When & Then
        mockMvc.perform(post("/api/v1/users")
                .contentType(MediaType.APPLICATION_JSON)
                .content(objectMapper.writeValueAsString(dto)))
                .andExpect(status().isCreated())
                .andExpect(jsonPath("$.code").value(0))
                .andExpect(jsonPath("$.data.username").value("testuser"))
                .andExpect(jsonPath("$.data.email").value("test@example.com"));
    }
    
    @Test
    void getUserById_ShouldReturnUser() throws Exception {
        // Given
        User user = new User();
        user.setUsername("testuser");
        user.setPassword(passwordEncoder.encode("password123"));
        user.setEmail("test@example.com");
        user = userRepository.save(user);
        
        // When & Then
        mockMvc.perform(get("/api/v1/users/{id}", user.getId()))
                .andExpect(status().isOk())
                .andExpect(jsonPath("$.code").value(0))
                .andExpect(jsonPath("$.data.id").value(user.getId()))
                .andExpect(jsonPath("$.data.username").value("testuser"));
    }
}
```

## 11. 性能优化规范

### 11.1 数据库查询优化
```java
// 使用分页查询
Page<User> findByStatus(UserStatus status, Pageable pageable);

// 使用JOIN FETCH避免N+1问题
@Query("SELECT u FROM User u LEFT JOIN FETCH u.roles WHERE u.id = :id")
Optional<User> findByIdWithRoles(@Param("id") Long id);

// 使用批量操作
@Modifying
@Query("UPDATE User u SET u.status = :status WHERE u.id IN :ids")
int batchUpdateStatus(@Param("ids") List<Long> ids, @Param("status") UserStatus status);
```

### 11.2 缓存使用
```java
@Service
@CacheConfig(cacheNames = "users")
public class UserServiceImpl implements UserService {
    
    @Override
    @Cacheable(key = "#id")
    public UserVO findById(Long id) {
        // ...
    }
    
    @Override
    @CachePut(key = "#result.id")
    public UserVO update(Long id, UserUpdateDTO dto) {
        // ...
    }
    
    @Override
    @CacheEvict(key = "#id")
    public void deleteById(Long id) {
        // ...
    }
    
    @Override
    @CacheEvict(allEntries = true)
    public void clearCache() {
        // 清空所有缓存
    }
}
```

## 12. 日志规范

### 12.1 日志级别使用
```java
@Slf4j
@Service
public class UserServiceImpl implements UserService {
    
    public UserVO findById(Long id) {
        log.debug("查询用户, ID: {}", id);
        
        User user = userRepository.findById(id)
                .orElseThrow(() -> {
                    log.warn("用户不存在, ID: {}", id);
                    return new BusinessException(ErrorCode.USER_NOT_FOUND);
                });
        
        log.info("成功查询用户, ID: {}, Username: {}", id, user.getUsername());
        
        return userMapper.toVO(user);
    }
    
    public UserVO create(UserCreateDTO dto) {
        try {
            log.info("创建用户, Username: {}", dto.getUsername());
            // 业务逻辑
        } catch (Exception e) {
            log.error("创建用户失败, Username: {}", dto.getUsername(), e);
            throw e;
        }
    }
}
```

## 13. API文档规范

### 13.1 Swagger配置
```java
@Configuration
@EnableOpenApi
public class SwaggerConfig {
    
    @Bean
    public OpenAPI customOpenAPI() {
        return new OpenAPI()
                .info(new Info()
                        .title("SpringBoot API")
                        .version("1.0.0")
                        .description("SpringBoot项目API文档")
                        .contact(new Contact()
                                .name("开发团队")
                                .email("dev@example.com")))
                .addSecurityItem(new SecurityRequirement().addList("Bearer"))
                .components(new Components()
                        .addSecuritySchemes("Bearer",
                                new SecurityScheme()
                                        .type(SecurityScheme.Type.HTTP)
                                        .scheme("bearer")
                                        .bearerFormat("JWT")));
    }
}
```

### 13.2 Controller文档注解
```java
@RestController
@RequestMapping("/api/v1/users")
@Tag(name = "用户管理", description = "用户相关接口")
public class UserController {
    
    @Operation(summary = "根据ID查询用户", description = "根据用户ID查询用户详细信息")
    @ApiResponses(value = {
            @ApiResponse(responseCode = "200", description = "查询成功"),
            @ApiResponse(responseCode = "404", description = "用户不存在")
    })
    @GetMapping("/{id}")
    public Result<UserVO> getById(
            @Parameter(description = "用户ID", required = true)
            @PathVariable Long id) {
        // ...
    }
}
```

## 14. 最佳实践总结

### 14.1 代码质量
- 遵循SOLID原则
- 保持代码简洁（KISS原则）
- 避免重复代码（DRY原则）
- 编写有意义的注释和文档
- 定期进行代码审查和重构

### 14.2 性能优化
- 合理使用缓存
- 优化数据库查询
- 使用异步处理耗时操作
- 避免N+1查询问题
- 使用连接池管理数据库连接

### 14.3 安全性
- 使用参数化查询防止SQL注入
- 对用户输入进行验证和转义
- 使用HTTPS传输敏感数据
- 密码加密存储
- 实施适当的访问控制

### 14.4 可维护性
- 保持一致的代码风格
- 编写清晰的文档
- 使用有意义的命名
- 保持方法简短和单一职责
- 定期更新依赖版本