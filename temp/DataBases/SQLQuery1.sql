Create Database DBTinTuc
use DBTinTuc

create table Loai_User(
	LoaiID varchar primary key,
	TenLoai nvarchar
)

create table QL_User (
	UserID varchar primary key,
	UserName varchar NOT NULL,
	Pw varchar NOT NULL,
	HoTen nvarchar NOT NULL,
	GioiTinh varchar,
	NgaySinh varchar,
	NgayTao date NOT NULL,
	LoaiID varchar NOT NULL,
	Email varchar,
	SDT varChar,
	FOREIGN KEY(LoaiID) REFERENCES Loai_User(LoaiID)
)

create table QL_LoaiBT(
	LoaiID varchar primary key,
	TenLoaiBT varchar
)

create table QL_BaiViet (

BaiVietID varchar primary key ,
UserID varchar NOT NULL,
NoiDung nvarchar,
ChuDe varchar,
NgayDangTin varchar,

FOREIGN KEY(ChuDe) REFERENCES QL_LoaiBT(LoaiID),
FOREIGN KEY(UserID) REFERENCES QL_User(UserID)
)
